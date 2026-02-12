# 🛒 Amazon Product Scraper

> Ứng dụng web mạnh mẽ để scrape sản phẩm từ Amazon với khả năng lọc theo giá, hỗ trợ đa tiền tệ, và giao diện trực quan.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Tính năng nổi bật

### 🎯 Scraping & Filtering
- ✅ **Scrape sản phẩm tự động** từ bất kỳ link tìm kiếm Amazon nào
- ✅ **Lọc theo giá linh hoạt**: Cao hơn, thấp hơn, hoặc chỉ lấy sản phẩm có giá
- ✅ **Hỗ trợ đa tiền tệ**: USD ($), VND (₫), EUR (€), GBP (£)
- ✅ **Phân trang thông minh**: Tự động scrape nhiều trang
- ✅ **Retry logic**: Tự động thử lại khi gặp lỗi 503

### 🎨 Giao diện & UX
- ✅ **Real-time logs**: Theo dõi tiến trình scraping trực tiếp
- ✅ **Nút dừng**: Dừng scraping bất cứ lúc nào
- ✅ **Responsive design**: Hoạt động mượt trên mọi thiết bị
- ✅ **Giao diện đẹp mắt**: Gradient background, animations mượt

### 📊 Export & Analytics
- ✅ **Xuất CSV**: Tải kết quả với đầy đủ thông tin
- ✅ **Thống kê chi tiết**: Số sản phẩm có giá/không giá
- ✅ **Link trực tiếp**: Click để xem sản phẩm trên Amazon

### 🛡️ Anti-detection
- ✅ **Random delays**: Giả lập hành vi người dùng thật
- ✅ **Dynamic headers**: Headers thay đổi theo tiền tệ
- ✅ **Session cookies**: Maintain state như browser
- ✅ **Referer tracking**: Giả lập click "Next page"

## 📋 Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **RAM**: 512MB+
- **Storage**: 50MB
- **Internet**: Kết nối ổn định

## 🚀 Cài đặt

### 1. Clone hoặc tải project

```bash
cd "AMZ Bot Diggy"
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Tạo favicon từ custom icon

**Nếu đã có icon PNG 512x512px:**
```bash
# Cài Pillow để resize
pip install Pillow

# Chạy script tạo favicon
python create_favicons.py
```

Script sẽ tự động tạo các kích thước:
- ✅ `favicon-16x16.png`
- ✅ `favicon-32x32.png`
- ✅ `favicon-48x48.png`
- ✅ `favicon-64x64.png`
- ✅ `apple-touch-icon.png` (180x180px)

**Hoặc tải online:**
- https://favicon.io/ (Dùng emoji hoặc text)
- https://realfavicongenerator.net/ (Upload logo)

Xem hướng dẫn chi tiết: `static/assets/icons/README.md`

### 4. Chạy ứng dụng

```bash
python app.py
```

### 5. Truy cập ứng dụng

Mở trình duyệt và truy cập: **http://localhost:5000**

## 📖 Hướng dẫn sử dụng

### Bước 1: Nhập thông tin cơ bản

#### 🔗 URL Amazon Search
Dán link tìm kiếm từ Amazon:
```
https://www.amazon.com/s?k=kitchen+products
https://www.amazon.com/s?k=laptop&rh=p_36:50000-
```

#### 🔢 Số lượng sản phẩm
- Nhập từ 1-100 sản phẩm
- **Khuyến nghị**: 10-30 sản phẩm để tránh bị block

### Bước 2: Chọn tiền tệ

#### 💱 Tiền tệ ưu tiên
Chọn loại tiền tệ bạn muốn scrape:

| Tiền tệ | Khi nào dùng | Ví dụ |
|---------|--------------|-------|
| **USD ($)** | Amazon.com, IP US | $299.99 |
| **VND (₫)** | Amazon từ Việt Nam | 7.500.000₫ |
| **EUR (€)** | Amazon EU | €249.99 |
| **GBP (£)** | Amazon UK | £199.99 |

💡 **Tip**: Nếu bạn ở Việt Nam nhưng muốn giá USD, hãy dùng VPN US.

### Bước 3: Lọc theo giá (Tùy chọn)

#### 💰 Giá mục tiêu
Nhập mức giá theo tiền tệ đã chọn ở bước 2.

#### 🎚️ Lọc theo giá

| Tùy chọn | Mô tả | Ví dụ |
|----------|-------|-------|
| **Tất cả sản phẩm** | Không lọc, lấy tất cả | - |
| **Chỉ sản phẩm có giá** | Bỏ qua sản phẩm "N/A" | Lấy sản phẩm có giá hiển thị |
| **Giá cao hơn mức đã điền** | Giá > target | Target: $100 → Lấy $150, $200 |
| **Giá thấp hơn mức đã điền** | Giá < target | Target: $100 → Lấy $50, $80 |

### Bước 4: Scrape!

1. Click **"Bắt đầu Scrape" 🚀**
2. Xem real-time logs trong phần "Processing Log"
3. Sản phẩm sẽ xuất hiện dần trong phần "Kết quả"
4. Click **"Dừng" ⏹️** nếu muốn dừng giữa chừng

### Bước 5: Xuất kết quả

Click **"Xuất CSV"** để tải file với format:
```csv
STT,Tên sản phẩm,Giá,Tiền tệ,Link
1,"Product Name",299.99,USD,https://...
```

## 🎓 Ví dụ sử dụng

### Case 1: Tìm laptop giá cao (> $1000)
```
URL: https://www.amazon.com/s?k=laptop
Số lượng: 20
Tiền tệ: USD ($)
Giá mục tiêu: 1000
Lọc: Giá cao hơn mức đã điền
```

### Case 2: Tìm TV giá rẻ (< $500)
```
URL: https://www.amazon.com/s?k=television
Số lượng: 15
Tiền tệ: USD ($)
Giá mục tiêu: 500
Lọc: Giá thấp hơn mức đã điền
```

### Case 3: Lấy tất cả sản phẩm có giá
```
URL: https://www.amazon.com/s?k=kitchen
Số lượng: 30
Tiền tệ: USD ($)
Lọc: Chỉ sản phẩm có giá
```

## 🛠️ Công nghệ sử dụng

### Backend
- **Flask 3.0.0**: Web framework
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP client
- **Python 3.8+**: Core language

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling (Grid, Flexbox, Animations)
- **JavaScript (Vanilla)**: No frameworks, pure JS
- **Server-Sent Events (SSE)**: Real-time communication

### Key Features
- **Session Management**: Maintain cookies like browser
- **Retry Logic**: Auto-retry on 503 errors
- **Multi-currency Support**: Dynamic headers & cookies
- **Anti-bot Detection**: Random delays, referer tracking

## ⚠️ Lưu ý quan trọng

### Về Amazon
- ⚠️ **Rate limiting**: Không scrape quá 50 sản phẩm một lúc
- ⚠️ **503 errors**: Đợi 5-10 phút nếu gặp lỗi này
- ⚠️ **IP blocking**: Dùng VPN nếu bị block nhiều lần
- ⚠️ **Giá N/A**: Một số sản phẩm không hiển thị giá công khai

### Best Practices
- ✅ Delay ít nhất 2-3 phút giữa các lần scrape
- ✅ Chọn đúng currency matching với region
- ✅ Dùng VPN để scrape từ region khác
- ✅ Scrape vào giờ thấp điểm (2-5 AM EST)

### Legal
- 📜 Chỉ dùng cho mục đích nghiên cứu/cá nhân
- 📜 Tuân thủ Amazon Terms of Service
- 📜 Không sử dụng cho mục đích thương mại lớn
- 📜 Tôn trọng robots.txt của Amazon

## 🐛 Troubleshooting

### ❌ Không scrape được sản phẩm

**Triệu chứng**: Log hiển thị "Tìm thấy 0 sản phẩm"

**Giải pháp**:
1. Kiểm tra URL có đúng format không
2. Thử copy URL trực tiếp từ thanh địa chỉ browser
3. Đảm bảo URL có chứa `/s?k=...`

### ❌ Lỗi 503 Service Unavailable

**Triệu chứng**: "Đã thử 3 lần nhưng vẫn bị lỗi 503"

**Giải pháp**:
1. Đợi 5-10 phút rồi thử lại
2. Giảm số lượng sản phẩm xuống 10-20
3. Kết nối VPN đổi IP
4. Thử vào giờ khác trong ngày

### ❌ Tất cả sản phẩm đều "N/A" (Không có giá)

**Triệu chứng**: Log hiển thị "Có giá: 0, Không giá: X"

**Nguyên nhân**: Amazon không hiển thị giá USD cho region của bạn

**Giải pháp**:
1. **Đổi tiền tệ**: Chọn VND nếu bạn ở Việt Nam
2. **Dùng VPN**: Kết nối VPN US để scrape USD
3. **Thử link khác**: Một số category không show giá
4. **Chọn "Tất cả sản phẩm"**: Lấy cả N/A để xem

### ❌ Giá sai tiền tệ

**Triệu chứng**: Chọn USD nhưng hiển thị VND

**Giải pháp**:
1. Reload trang với **Ctrl + F5**
2. Dùng VPN matching với currency
3. Clear browser cookies của Amazon
4. Thử Incognito/Private mode

### ❌ CSV không tải được

**Triệu chứng**: Click "Xuất CSV" không có gì xảy ra

**Giải pháp**:
1. Kiểm tra popup blocker của browser
2. Thử browser khác (Chrome, Firefox)
3. Mở Console (F12) xem lỗi
4. Đảm bảo đã scrape ít nhất 1 sản phẩm

## 💡 Tips & Tricks

### Scraping hiệu quả
1. 🔥 **Warm-up**: Scrape 5 sản phẩm trước, sau đó scrape số lượng lớn
2. 🌙 **Off-peak hours**: Scrape vào 2-5 AM EST để ít bị block
3. 🔄 **Rotate IPs**: Dùng nhiều VPN/proxy khác nhau
4. ⏰ **Time gaps**: Đợi 3-5 phút giữa các session

### Tìm giá tốt
1. 💰 **Price range**: Dùng Amazon URL filter: `&rh=p_36:50000-100000` (50-100k cents = $500-$1000)
2. 🏷️ **Deals**: Search với `&s=price-asc-rank` để sắp xếp theo giá
3. 📊 **Compare**: Scrape nhiều lần trong ngày để track giá

### Debug
1. 🔍 **Console**: Mở F12 → Console để xem logs chi tiết
2. 🌐 **Network**: Tab Network để xem requests
3. 📝 **Server logs**: Xem terminal Python để debug backend

## 📊 Kết quả mẫu

### Success case
```
✅ Hoàn thành! Đã scrape 30 sản phẩm (Có giá: 28, Không giá: 2)
Trang 1: 15 sản phẩm (Có giá: 14, Không giá: 1)
Trang 2: 15 sản phẩm (Có giá: 14, Không giá: 1)
```

### CSV Output
| STT | Tên sản phẩm | Giá | Tiền tệ | Link |
|-----|--------------|-----|---------|------|
| 1 | Samsung 65" QLED TV | 1299.99 | USD | [Link] |
| 2 | LG 55" OLED TV | 1499.99 | USD | [Link] |

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📝 Changelog

### v2.0.0 (Current)
- ✨ Multi-currency support (USD, VND, EUR, GBP)
- ✨ Stop button để dừng scraping
- ✨ Retry logic cho 503 errors
- ✨ Improved price detection (4 methods)
- ✨ Better statistics & logging
- 🐛 Fixed duplicate page parameter
- 🐛 Fixed JSON encoding issues

### v1.0.0
- 🎉 Initial release
- Basic scraping functionality
- CSV export
- Price filtering

## 📄 License

MIT License - Tự do sử dụng cho mục đích cá nhân và giáo dục.

**Lưu ý**: Vui lòng tuân thủ Amazon Terms of Service và không sử dụng cho mục đích thương mại vi phạm.

## 👨‍💻 Author

Made with ❤️ by Diggy

## 🙏 Acknowledgments

- Amazon for the data source
- Flask community
- BeautifulSoup4 team
- Open source community

---

**⭐ Nếu bạn thấy hữu ích, hãy để lại một star!**

**📧 Có câu hỏi? Tạo issue trên GitHub!**
