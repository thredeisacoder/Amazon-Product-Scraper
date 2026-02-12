let products = [];
let eventSource = null;
let currentReader = null;
let isScrapingActive = false;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('scrapeForm');
    const scrapeBtn = document.getElementById('scrapeBtn');
    const stopBtn = document.getElementById('stopBtn');
    const clearLogBtn = document.getElementById('clearLog');
    const exportBtn = document.getElementById('exportBtn');
    
    form.addEventListener('submit', handleSubmit);
    stopBtn.addEventListener('click', stopScraping);
    clearLogBtn.addEventListener('click', clearLog);
    exportBtn.addEventListener('click', exportToCSV);
});

function handleSubmit(e) {
    e.preventDefault();
    
    // Reset
    products = [];
    clearLog();
    document.getElementById('resultsContent').innerHTML = '';
    document.getElementById('productCount').textContent = '0';
    
    // Hiển thị containers
    document.getElementById('logContainer').style.display = 'block';
    document.getElementById('resultsContainer').style.display = 'block';
    
    // Lấy dữ liệu form
    const formData = {
        url: document.getElementById('url').value,
        max_products: document.getElementById('max_products').value,
        target_price: document.getElementById('target_price').value || null,
        price_filter: document.getElementById('price_filter').value,
        preferred_currency: document.getElementById('preferred_currency').value
    };
    
    // Update buttons
    const scrapeBtn = document.getElementById('scrapeBtn');
    const stopBtn = document.getElementById('stopBtn');
    
    scrapeBtn.disabled = true;
    scrapeBtn.innerHTML = '<span class="loading"></span><span>Đang scrape...</span>';
    stopBtn.style.display = 'inline-flex';
    
    isScrapingActive = true;
    
    // Start scraping
    startScraping(formData);
}

function startScraping(formData) {
    // Close existing connection
    if (eventSource) {
        eventSource.close();
    }
    
    if (currentReader) {
        currentReader.cancel();
    }
    
    // Create EventSource for Server-Sent Events
    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        const reader = response.body.getReader();
        currentReader = reader;
        const decoder = new TextDecoder();
        
        function readStream() {
            if (!isScrapingActive) {
                reader.cancel();
                enableButton();
                return;
            }
            
            reader.read().then(({ done, value }) => {
                if (done) {
                    enableButton();
                    return;
                }
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n\n');
                
                lines.forEach(line => {
                    if (line.startsWith('data: ') && line.trim().length > 6) {
                        try {
                            const jsonData = line.substring(6).trim();
                            const result = JSON.parse(jsonData);
                            handleScrapingResult(result);
                        } catch (e) {
                            console.error('Error parsing JSON:', e);
                            console.error('Raw data:', line.substring(6));
                            addLog('error', 'Lỗi parse dữ liệu từ server');
                        }
                    }
                });
                
                readStream();
            }).catch(error => {
                if (error.name !== 'AbortError') {
                    console.error('Stream error:', error);
                }
            });
        }
        
        readStream();
    })
    .catch(error => {
        addLog('error', `Lỗi kết nối: ${error.message}`);
        enableButton();
    });
}

function stopScraping() {
    isScrapingActive = false;
    
    if (currentReader) {
        currentReader.cancel();
        currentReader = null;
    }
    
    addLog('error', 'Đã dừng scraping bởi người dùng');
    enableButton();
}

function handleScrapingResult(result) {
    switch(result.type) {
        case 'log':
            addLog('log', result.message);
            break;
            
        case 'error':
            addLog('error', result.message);
            break;
            
        case 'product':
            addLog('product', `Đã tìm thấy sản phẩm ${result.count}: ${result.data.title.substring(0, 50)}...`);
            addProduct(result.data);
            break;
            
        case 'complete':
            addLog('success', result.message);
            enableButton();
            break;
    }
}

function addLog(type, message) {
    const logContent = document.getElementById('logContent');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    
    let icon = '📝';
    if (type === 'error') icon = '❌';
    if (type === 'success') icon = '✅';
    if (type === 'product') icon = '📦';
    
    const timestamp = new Date().toLocaleTimeString('vi-VN');
    
    logEntry.innerHTML = `
        <span class="log-icon">${icon}</span>
        <span>[${timestamp}] ${message}</span>
    `;
    
    logContent.appendChild(logEntry);
    logContent.scrollTop = logContent.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function addProduct(product) {
    try {
        // Validate product data
        if (!product || !product.title || !product.url) {
            console.error('Invalid product data:', product);
            addLog('error', 'Lỗi: Dữ liệu sản phẩm không hợp lệ');
            return;
        }
        
        products.push(product);
        
        const resultsContent = document.getElementById('resultsContent');
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        
        // Format price with correct currency
        let priceHtml;
        if (product.price && typeof product.price === 'number') {
            const currency = product.currency || 'USD';
            let priceFormatted;
            
            try {
                if (currency === 'VND') {
                    // VND format: 1.234.567₫ (no decimals)
                    priceFormatted = Math.round(product.price).toLocaleString('vi-VN') + '₫';
                } else if (currency === 'USD') {
                    priceFormatted = '$' + product.price.toFixed(2);
                } else if (currency === 'EUR') {
                    priceFormatted = '€' + product.price.toFixed(2);
                } else if (currency === 'GBP') {
                    priceFormatted = '£' + product.price.toFixed(2);
                } else {
                    priceFormatted = product.price.toFixed(2) + ' ' + currency;
                }
                
                priceHtml = `<div class="product-price">${priceFormatted}</div>`;
            } catch (e) {
                console.error('Error formatting price:', e);
                priceHtml = `<div class="product-price no-price">Lỗi định dạng giá</div>`;
            }
        } else {
            priceHtml = `<div class="product-price no-price">Không có giá</div>`;
        }
        
        // Escape HTML to prevent injection
        const safeTitle = escapeHtml(product.title);
        const safeUrl = escapeHtml(product.url);
        
        productCard.innerHTML = `
            <span class="product-number">#${products.length}</span>
            <div class="product-title">${safeTitle}</div>
            ${priceHtml}
            <a href="${safeUrl}" target="_blank" class="product-link">
                Xem trên Amazon →
            </a>
        `;
        
        resultsContent.appendChild(productCard);
        document.getElementById('productCount').textContent = products.length;
        
        console.log(`Added product #${products.length}:`, product.title);
        
    } catch (error) {
        console.error('Error adding product:', error, product);
        addLog('error', `Lỗi khi thêm sản phẩm: ${error.message}`);
    }
}

function clearLog() {
    document.getElementById('logContent').innerHTML = '';
}

function enableButton() {
    const scrapeBtn = document.getElementById('scrapeBtn');
    const stopBtn = document.getElementById('stopBtn');
    
    scrapeBtn.disabled = false;
    scrapeBtn.innerHTML = '<span class="btn-text">Bắt đầu Scrape</span><span class="btn-icon">🚀</span>';
    stopBtn.style.display = 'none';
    
    isScrapingActive = false;
    currentReader = null;
}

function exportToCSV() {
    if (products.length === 0) {
        alert('Không có dữ liệu để xuất!');
        return;
    }
    
    // Create CSV content
    let csv = 'STT,Tên sản phẩm,Giá,Tiền tệ,Link\n';
    
    products.forEach((product, index) => {
        const currency = product.currency || 'USD';
        let price;
        
        if (product.price) {
            if (currency === 'VND') {
                price = Math.round(product.price);
            } else {
                price = product.price.toFixed(2);
            }
        } else {
            price = 'N/A';
        }
        
        const title = `"${product.title.replace(/"/g, '""')}"`;
        csv += `${index + 1},${title},${price},${currency},${product.url}\n`;
    });
    
    // Create download link
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    link.setAttribute('href', url);
    link.setAttribute('download', `amazon_products_${timestamp}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    addLog('success', `Đã xuất ${products.length} sản phẩm ra file CSV`);
}
