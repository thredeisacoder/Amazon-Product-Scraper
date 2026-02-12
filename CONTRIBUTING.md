# Contributing to Amazon Product Scraper

Thank you for your interest in contributing! 🎉

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic knowledge of Flask and web scraping

### Setup Development Environment

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/amz-bot-diggy.git
   cd amz-bot-diggy
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

### Commit Messages
Use semantic commit messages:
```
feat: Add new currency support
fix: Resolve 503 error handling
docs: Update README with examples
style: Format code with black
refactor: Simplify price extraction logic
test: Add unit tests for scraping
chore: Update dependencies
```

### Branch Naming
```
feature/your-feature-name
bugfix/issue-description
hotfix/critical-fix
docs/documentation-update
```

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clean, documented code
   - Test thoroughly
   - Update README if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add amazing feature"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Wait for review

## 🐛 Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error logs/screenshots

## 💡 Suggesting Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md) and describe:
- The problem you're trying to solve
- Your proposed solution
- Alternative approaches
- Willingness to contribute

## 🧪 Testing

Before submitting:
- [ ] Test on multiple browsers
- [ ] Test with different Amazon URLs
- [ ] Test price filtering
- [ ] Test currency switching
- [ ] Test error handling
- [ ] Verify no console errors

## 📚 Documentation

If adding features:
- Update README.md
- Add inline code comments
- Update docstrings
- Add examples if needed

## ⚠️ Important Notes

### Legal Compliance
- Respect Amazon's Terms of Service
- Do not enable mass scraping
- Add rate limiting for new features
- Document ethical usage

### Performance
- Avoid blocking operations
- Use async where appropriate
- Minimize memory usage
- Test with large datasets

### Security
- Never commit API keys or secrets
- Sanitize user inputs
- Validate all data
- Use secure dependencies

## 🎯 Areas for Contribution

### High Priority
- [ ] Add more currency support
- [ ] Improve error handling
- [ ] Add unit tests
- [ ] Performance optimization
- [ ] Better mobile UI

### Medium Priority
- [ ] Add export to Excel
- [ ] Add price history tracking
- [ ] Add product comparison
- [ ] Add bookmark feature
- [ ] Dark mode

### Low Priority
- [ ] Add more scraping sources
- [ ] Add scheduling
- [ ] Add notifications
- [ ] Add database support

## 💬 Questions?

- Open a [GitHub Issue](https://github.com/YOUR-USERNAME/amz-bot-diggy/issues)
- Check existing issues first
- Be respectful and patient

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy

## 🙏 Thank You!

Every contribution, no matter how small, is valued and appreciated!

---

**Happy Coding! 🚀**
