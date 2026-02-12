from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

app = Flask(__name__)

def clean_url_params(url, remove_params=['page']):
    """Remove specific parameters from URL"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
    # Remove specified params
    for param in remove_params:
        query_params.pop(param, None)
    
    # Rebuild URL
    new_query = urlencode(query_params, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

def get_headers(preferred_currency='USD'):
    """Tạo headers dựa trên tiền tệ ưu tiên"""
    # Map currency to Accept-Language and location
    currency_config = {
        'USD': {
            'accept_language': 'en-US,en;q=0.9',
            'cloudfront_viewer_country': 'US'
        },
        'VND': {
            'accept_language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'cloudfront_viewer_country': 'VN'
        },
        'EUR': {
            'accept_language': 'de-DE,de;q=0.9,en;q=0.8',
            'cloudfront_viewer_country': 'DE'
        },
        'GBP': {
            'accept_language': 'en-GB,en;q=0.9',
            'cloudfront_viewer_country': 'GB'
        }
    }
    
    config = currency_config.get(preferred_currency, currency_config['USD'])
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': config['accept_language'],
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    return headers

def extract_price(price_text):
    """Trích xuất giá từ text, trả về tuple (giá, currency)"""
    if not price_text:
        return None, None
    
    # Remove whitespace
    price_text = price_text.strip()
    
    # Detect currency
    currency = 'USD'  # Default
    if '₫' in price_text or 'VND' in price_text or 'đ' in price_text:
        currency = 'VND'
    elif '$' in price_text or 'USD' in price_text:
        currency = 'USD'
    elif '€' in price_text or 'EUR' in price_text:
        currency = 'EUR'
    elif '£' in price_text or 'GBP' in price_text:
        currency = 'GBP'
    
    # Extract number based on currency
    if currency == 'VND':
        # VND format: 1.234.567 hoặc 1,234,567 (không có decimal)
        price_match = re.search(r'(\d{1,3}(?:[,\.]\d{3})+)', price_text)
        if price_match:
            price_str = price_match.group(1).replace('.', '').replace(',', '')
            try:
                return float(price_str), currency
            except ValueError:
                return None, None
    else:
        # USD/EUR/GBP format: 1,234.56 hoặc 1234.56
        # Remove currency symbols
        clean_text = re.sub(r'[^\d,\.]', '', price_text)
        
        # Handle formats: 1,234.56 or 1.234,56
        if ',' in clean_text and '.' in clean_text:
            # Determine which is thousand separator
            comma_pos = clean_text.rfind(',')
            dot_pos = clean_text.rfind('.')
            if dot_pos > comma_pos:
                # Format: 1,234.56
                clean_text = clean_text.replace(',', '')
            else:
                # Format: 1.234,56
                clean_text = clean_text.replace('.', '').replace(',', '.')
        elif ',' in clean_text:
            # Check if it's decimal or thousand separator
            parts = clean_text.split(',')
            if len(parts[-1]) == 2:
                # Likely decimal: 123,45
                clean_text = clean_text.replace(',', '.')
            else:
                # Likely thousand: 1,234
                clean_text = clean_text.replace(',', '')
        
        try:
            return float(clean_text), currency
        except ValueError:
            return None, None
    
    return None, None

def scrape_amazon_products(url, max_products=10, target_price=None, price_filter='all', preferred_currency='USD'):
    """Scrape sản phẩm từ Amazon"""
    products = []
    page = 1
    total_with_price = 0
    total_no_price = 0
    
    # Get headers dựa trên currency
    headers = get_headers(preferred_currency)
    
    # Create session with cookies to force currency
    session = requests.Session()
    session.headers.update(headers)
    
    # Set cookies to force currency preference
    cookies = {}
    if preferred_currency == 'USD':
        cookies = {
            'i18n-prefs': 'USD',
            'lc-main': 'en_US'
        }
    elif preferred_currency == 'VND':
        cookies = {
            'i18n-prefs': 'VND',
            'lc-main': 'vi_VN'
        }
    elif preferred_currency == 'EUR':
        cookies = {
            'i18n-prefs': 'EUR',
            'lc-main': 'de_DE'
        }
    elif preferred_currency == 'GBP':
        cookies = {
            'i18n-prefs': 'GBP',
            'lc-main': 'en_GB'
        }
    
    try:
        # Clean URL để remove page parameter cũ
        base_url = clean_url_params(url, ['page'])
        previous_url = None
        
        while len(products) < max_products:
            # Tạo URL cho từng trang
            if page == 1:
                current_url = base_url
            else:
                separator = '&' if '?' in base_url else '?'
                current_url = f"{base_url}{separator}page={page}"
            
            yield {
                'type': 'log',
                'message': f'Đang scrape trang {page} (Currency: {preferred_currency})'
            }
            
            # Retry logic cho 503 errors
            max_retries = 3
            retry_count = 0
            response = None
            
            while retry_count < max_retries:
                try:
                    # Random delay để tránh bị phát hiện là bot
                    if page > 1 or retry_count > 0:
                        delay = random.uniform(2, 4)
                        yield {
                            'type': 'log',
                            'message': f'Đợi {delay:.1f}s trước khi request...'
                        }
                        time.sleep(delay)
                    
                    # Thêm referer để giống như browsing thật
                    request_headers = headers.copy()
                    if previous_url and page > 1:
                        request_headers['Referer'] = previous_url
                    
                    # Gửi request với headers và cookies phù hợp
                    response = session.get(current_url, headers=request_headers, cookies=cookies, timeout=15)
                    
                    if response.status_code == 200:
                        break
                    elif response.status_code == 503:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = retry_count * 5  # 5s, 10s, 15s
                            yield {
                                'type': 'log',
                                'message': f'Gặp lỗi 503, thử lại lần {retry_count}/{max_retries} sau {wait_time}s...'
                            }
                            time.sleep(wait_time)
                        else:
                            yield {
                                'type': 'error',
                                'message': f'Đã thử {max_retries} lần nhưng vẫn bị lỗi 503. Amazon đang chặn requests. Gợi ý: Thử lại sau vài phút hoặc giảm số lượng sản phẩm.'
                            }
                            break
                    else:
                        yield {
                            'type': 'error',
                            'message': f'Lỗi khi truy cập trang {page}: Status code {response.status_code}'
                        }
                        break
                        
                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        yield {
                            'type': 'log',
                            'message': f'Lỗi kết nối, thử lại lần {retry_count}/{max_retries}...'
                        }
                        time.sleep(retry_count * 3)
                    else:
                        yield {
                            'type': 'error',
                            'message': f'Lỗi kết nối: {str(e)}'
                        }
                        break
            
            # Kiểm tra response
            if not response or response.status_code != 200:
                break
            
            # Lưu URL hiện tại làm referer cho request sau
            previous_url = current_url
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Tìm các sản phẩm
            # Amazon có nhiều cấu trúc khác nhau, thử nhiều selector
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            if not product_containers:
                yield {
                    'type': 'log',
                    'message': f'Không tìm thấy sản phẩm ở trang {page}, có thể đã hết kết quả'
                }
                break
            
            yield {
                'type': 'log',
                'message': f'Tìm thấy {len(product_containers)} sản phẩm ở trang {page}'
            }
            
            products_found_in_page = 0
            products_with_price = 0
            products_no_price = 0
            skipped_no_title = 0
            skipped_no_link = 0
            skipped_price_filter = 0
            
            for container in product_containers:
                if len(products) >= max_products:
                    break
                
                try:
                    # Lấy title - thử nhiều cách
                    title = None
                    title_link = None
                    
                    # Cách 1: Tìm h2 với class
                    h2_elem = container.find('h2', class_=lambda x: x and 'a-size' in x)
                    if h2_elem:
                        title_link = h2_elem.find('a')
                    
                    # Cách 2: Tìm h2 bất kỳ
                    if not title_link:
                        h2_elem = container.find('h2')
                        if h2_elem:
                            title_link = h2_elem.find('a')
                    
                    # Cách 3: Tìm trực tiếp a tag có class chứa 'a-link-normal'
                    if not title_link:
                        title_link = container.find('a', class_=lambda x: x and 'a-link-normal' in x and 's-line-clamp' in str(x))
                    
                    if not title_link:
                        skipped_no_link += 1
                        continue
                    
                    title = title_link.get_text(strip=True)
                    if not title:
                        skipped_no_title += 1
                        continue
                    
                    product_url = title_link.get('href', '')
                    if product_url:
                        if not product_url.startswith('http'):
                            product_url = urljoin('https://www.amazon.com', product_url)
                    else:
                        skipped_no_link += 1
                        continue
                    
                    # Lấy giá - thử nhiều cách
                    price = None
                    currency = preferred_currency  # Dùng currency đã chọn
                    
                    # Cách 1: Tìm offscreen price (thường chính xác nhất)
                    offscreen_spans = container.find_all('span', class_='a-offscreen')
                    for offscreen in offscreen_spans:
                        price_text = offscreen.get_text(strip=True)
                        temp_price, temp_currency = extract_price(price_text)
                        if temp_price is not None:
                            price = temp_price
                            currency = temp_currency
                            break
                    
                    # Cách 2: Tìm span a-price-whole và a-price-fraction
                    if price is None:
                        price_whole = container.find('span', class_='a-price-whole')
                        if price_whole:
                            price_text = price_whole.get_text(strip=True)
                            price_fraction = container.find('span', class_='a-price-fraction')
                            if price_fraction:
                                price_text = price_text + price_fraction.get_text(strip=True)
                            
                            # Tìm currency symbol
                            price_symbol = container.find('span', class_='a-price-symbol')
                            if price_symbol:
                                price_text = price_symbol.get_text(strip=True) + price_text
                            
                            price, currency = extract_price(price_text)
                    
                    # Cách 3: Tìm span a-price (toàn bộ)
                    if price is None:
                        price_spans = container.find_all('span', class_='a-price')
                        for price_span in price_spans:
                            price_text = price_span.get_text(strip=True)
                            temp_price, temp_currency = extract_price(price_text)
                            if temp_price is not None:
                                price = temp_price
                                currency = temp_currency
                                break
                    
                    # Cách 4: Tìm bất kỳ text chứa $ và số
                    if price is None:
                        container_text = container.get_text()
                        # Tìm pattern $XX.XX hoặc $XXX
                        price_patterns = [
                            r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
                            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*\$'
                        ]
                        for pattern in price_patterns:
                            match = re.search(pattern, container_text)
                            if match:
                                price, currency = extract_price(match.group(0))
                                if price is not None:
                                    break
                    
                    # Kiểm tra điều kiện lọc giá
                    # Filter: Chỉ sản phẩm có giá
                    if price_filter == 'has_price':
                        if price is None:
                            skipped_price_filter += 1
                            continue
                    
                    # Filter: Theo mức giá (above/below PHẢI có giá)
                    if price_filter in ['above', 'below']:
                        if price is None:
                            # Không có giá thì bỏ qua khi filter above/below
                            skipped_price_filter += 1
                            continue
                        
                        if target_price is not None:
                            if price_filter == 'above' and price <= target_price:
                                skipped_price_filter += 1
                                continue
                            elif price_filter == 'below' and price >= target_price:
                                skipped_price_filter += 1
                                continue
                    
                    product_data = {
                        'title': title,
                        'url': product_url,
                        'price': price,
                        'currency': currency
                    }
                    
                    products.append(product_data)
                    products_found_in_page += 1
                    current_count = len(products)
                    
                    # Track có giá hay không
                    if price is not None:
                        products_with_price += 1
                        total_with_price += 1
                    else:
                        products_no_price += 1
                        total_no_price += 1
                    
                    # Log trước khi yield
                    price_display = f"${price:.2f}" if price else "N/A"
                    yield {
                        'type': 'log',
                        'message': f'Sản phẩm #{current_count}: {title[:50]}... (Giá: {price_display})'
                    }
                    
                    # Yield product data
                    try:
                        yield {
                            'type': 'product',
                            'data': product_data,
                            'count': current_count
                        }
                    except Exception as ye:
                        yield {
                            'type': 'error',
                            'message': f'Lỗi khi gửi dữ liệu sản phẩm #{current_count}: {str(ye)}'
                        }
                    
                except Exception as e:
                    yield {
                        'type': 'error',
                        'message': f'Lỗi khi xử lý sản phẩm: {str(e)}'
                    }
                    continue
            
            # Log chi tiết
            debug_msg = f'Trang {page}: Lấy được {products_found_in_page}/{len(product_containers)} sản phẩm'
            
            # Thêm thông tin về giá
            if products_found_in_page > 0:
                debug_msg += f' (Có giá: {products_with_price}, Không giá: {products_no_price})'
            
            # Thông tin skip
            skip_details = []
            if skipped_no_link > 0:
                skip_details.append(f'{skipped_no_link} không có link')
            if skipped_no_title > 0:
                skip_details.append(f'{skipped_no_title} không có title')
            if skipped_price_filter > 0:
                skip_details.append(f'{skipped_price_filter} lọc giá')
            
            if skip_details:
                debug_msg += f', Bỏ qua: {", ".join(skip_details)}'
            
            yield {
                'type': 'log',
                'message': debug_msg
            }
            
            # Nếu đã đủ số lượng sản phẩm, dừng lại
            if len(products) >= max_products:
                break
            
            # Tăng trang
            page += 1
        
        # Summary message
        summary = f'Hoàn thành! Đã scrape {len(products)} sản phẩm'
        if total_with_price > 0 or total_no_price > 0:
            summary += f' (Có giá: {total_with_price}, Không giá: {total_no_price})'
        
        yield {
            'type': 'complete',
            'message': summary,
            'total': len(products),
            'with_price': total_with_price,
            'no_price': total_no_price
        }
        
        # Cảnh báo nếu không tìm thấy sản phẩm nào có giá khi đang filter theo giá
        if total_with_price == 0 and total_no_price > 0 and price_filter in ['above', 'below', 'has_price']:
            yield {
                'type': 'log',
                'message': f'⚠️ Cảnh báo: Không tìm thấy sản phẩm nào có giá. Amazon có thể không hiển thị giá {preferred_currency} cho region của bạn. Thử: (1) Thay đổi tiền tệ, (2) Dùng VPN, hoặc (3) Chọn "Tất cả sản phẩm".'
            }
        
    except Exception as e:
        yield {
            'type': 'error',
            'message': f'Lỗi: {str(e)}'
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('url', '')
        max_products = int(data.get('max_products', 10))
        target_price = data.get('target_price')
        price_filter = data.get('price_filter', 'all')
        preferred_currency = data.get('preferred_currency', 'USD')
        
        if target_price:
            target_price = float(target_price)
        
        if not url:
            return jsonify({'error': 'URL không được để trống'}), 400
        
        def generate():
            for result in scrape_amazon_products(url, max_products, target_price, price_filter, preferred_currency):
                try:
                    json_data = json.dumps(result, ensure_ascii=False)
                    yield f"data: {json_data}\n\n"
                except Exception as e:
                    error_msg = json.dumps({'type': 'error', 'message': f'Lỗi JSON encode: {str(e)}'})
                    yield f"data: {error_msg}\n\n"
        
        return app.response_class(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
