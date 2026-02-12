# 🎨 Icons & Favicon

Folder này chứa các icon và favicon cho ứng dụng.

## 📁 Các file cần có:

### Favicon (Required)
- `favicon-16x16.png` - Icon 16x16px (hiển thị trên tab browser)
- `favicon-32x32.png` - Icon 32x32px (hiển thị trên tab browser)
- `apple-touch-icon.png` - Icon 180x180px (iOS home screen)

### Optional
- `favicon.ico` - Icon format ICO (fallback cho browser cũ)
- `logo.png` - Logo chính của ứng dụng
- `logo.svg` - Logo dạng vector

## 🎨 Design Guidelines

### Theme
- **Primary Color**: #FF9900 (Amazon Orange)
- **Secondary Color**: #146EB4 (Blue)
- **Background**: Gradient Purple to Blue

### Icon Concept
Các ý tưởng cho icon:
1. 🛒 Shopping cart với "A" letter
2. 📦 Package/box với search icon
3. 🤖 Robot với Amazon "A" smile
4. 📊 Chart/analytics với shopping icon

## 🔧 Cách tạo Favicon

### Option 1: Online Tools (Dễ nhất)
1. Truy cập: https://favicon.io/
2. Upload logo hoặc tạo text-based icon
3. Download và extract vào folder này

### Option 2: Canva
1. Mở Canva → Custom size 512x512px
2. Design icon của bạn
3. Export PNG
4. Resize bằng online tool về các size cần thiết

### Option 3: Figma/Adobe
1. Design icon 512x512px
2. Export multiple sizes:
   - 16x16px → `favicon-16x16.png`
   - 32x32px → `favicon-32x32.png`
   - 180x180px → `apple-touch-icon.png`

## 🖼️ Icon Template

Sử dụng emoji tạm thời (đã có trong HTML):
```
🛒 - Shopping cart (đang dùng)
```

Hoặc tạo SVG đơn giản:
- Background: #667eea to #764ba2 (gradient)
- Text: "AMZ" hoặc "A" màu trắng
- Font: Bold, Sans-serif

## ✅ Checklist

Sau khi thêm icons:
- [ ] `favicon-16x16.png` có trong folder
- [ ] `favicon-32x32.png` có trong folder
- [ ] `apple-touch-icon.png` có trong folder
- [ ] Test trên browser (Ctrl+F5 để clear cache)
- [ ] Test trên mobile
- [ ] Icons hiển thị đúng trên tab browser

## 💡 Tips

- **Format**: Dùng PNG với transparent background
- **Quality**: Xuất ở độ phân giải cao rồi resize
- **File size**: Nên < 50KB mỗi file
- **Colors**: Dùng brand colors để nhận diện
- **Simple**: Icon nhỏ nên design đơn giản, dễ nhận diện

## 📚 Resources

### Free Icon Tools
- https://favicon.io/ - Generate favicon
- https://realfavicongenerator.net/ - Advanced favicon generator
- https://www.canva.com/ - Design tool
- https://www.figma.com/ - Professional design

### Icon Libraries
- https://iconscout.com/
- https://flaticon.com/
- https://icons8.com/

## 🎯 Current Status

- ✅ HTML updated with favicon links
- ⏳ Icons pending (add your icons here)
- 📝 Using emoji 🛒 as temporary icon in page title

---

**Need help?** Check the main README.md for full documentation.
