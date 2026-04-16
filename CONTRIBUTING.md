# Contributing to IPL Match Tracker

Thank you for your interest in contributing! Here's how you can help:

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/exciting-cricket-matches-tracker.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep lines under 100 characters

### Testing
- Write tests for new features
- Place tests in `tests/` directory
- Run tests before submitting PR:
  ```bash
  python tests/test_telegram.py
  python tests/test_api.py
  python tests/test_excitement.py
  ```

### Commit Messages
- Use clear, descriptive commit messages
- Format: `feat: add feature X` or `fix: resolve issue Y`
- Examples:
  - `feat: add Discord notification support`
  - `fix: resolve Telegram timeout issue`
  - `docs: update installation instructions`

## Types of Contributions

### 🐛 Bug Fixes
- Describe the bug clearly
- Include steps to reproduce
- Propose a fix if possible
- Include relevant logs

### ✨ Features
- Describe the feature and its benefits
- Explain how it works
- Consider backward compatibility
- Include tests for new functionality

### 📚 Documentation
- Fix typos and unclear sections
- Add examples and use cases
- Improve setup instructions
- Add API documentation

### 🎨 Code Quality
- Refactor code for clarity
- Remove technical debt
- Improve performance
- Add type hints

## Pull Request Process

1. **Update tests** - Add tests for your changes
2. **Update docs** - Update README if behavior changes
3. **Clean up** - Remove debug code and unused imports
4. **Test locally** - Run all tests before submitting
5. **Write PR description** - Explain what and why

## Areas for Contribution

### High Priority
- [ ] Machine learning-based excitement prediction
- [ ] Support for other cricket leagues
- [ ] Web dashboard UI
- [ ] Performance optimization

### Medium Priority
- [ ] Multi-language support
- [ ] Discord/WhatsApp integration
- [ ] Database storage for historical data
- [ ] Match statistics and analytics

### Low Priority
- [ ] UI improvements
- [ ] Documentation enhancements
- [ ] Code refactoring
- [ ] Test coverage expansion

## Questions?

- Check existing issues
- Read the README and docs
- Open a discussion issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Happy contributing! 🏏
