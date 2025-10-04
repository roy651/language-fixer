# PyPI Publishing Checklist

## ✅ Pre-Publish (Already Done!)

- [x] Package built successfully
- [x] GitHub URLs updated in pyproject.toml
- [x] Package validation passed
- [x] Version: 0.2.0

## 📝 Publishing Steps

### 1. Create PyPI Account (One-time)
- Go to https://pypi.org/account/register/
- Verify email address

### 2. Create API Token (One-time)
- Go to https://pypi.org/manage/account/token/
- Click "Add API token"
- Name: "language-fixer"
- Scope: "Entire account"
- **COPY THE TOKEN** (shown only once!)

### 3. Upload to PyPI

```bash
uv run twine upload dist/*
```

When prompted:
- **Username**: `__token__`
- **Password**: `<paste your API token>`

### 4. Verify Publication
- Visit: https://pypi.org/project/language-fixer/
- Test install:
  ```bash
  pipx install language-fixer
  language-fixer --help
  ```

## 🧪 Optional: Test on Test PyPI First

If you want to test before publishing to production PyPI:

### 1. Create Test PyPI Account
- Go to https://test.pypi.org/account/register/

### 2. Create Test API Token
- Go to https://test.pypi.org/manage/account/token/

### 3. Upload to Test PyPI
```bash
uv run twine upload --repository testpypi dist/*
```

### 4. Test Installation
```bash
pip install --index-url https://test.pypi.org/simple/ language-fixer
```

## 🔄 Publishing Updates (Future)

When you need to publish a new version:

1. **Update version** in:
   - `pyproject.toml`
   - `src/language_fixer/__init__.py`

2. **Clean and rebuild**:
   ```bash
   rm -rf dist/
   uv run python -m build
   uv run twine check dist/*
   ```

3. **Upload**:
   ```bash
   uv run twine upload dist/*
   ```

## 📦 What Gets Installed

When users run `pipx install language-fixer`, they get:

- **Commands**:
  - `language-fixer` - Main application
  - `language-fixer-generate-mapping` - Mapping generator
  - `language-fixer-install-service` - Service installer
  - `language-fixer-uninstall-service` - Service uninstaller

- **Package contents**:
  - Python modules
  - Language mappings (Hebrew, Arabic, Russian)
  - Config example file

## 🎯 User Experience After Publishing

```bash
# Install
pipx install language-fixer

# Setup as service
language-fixer-install-service

# Grant accessibility permissions (macOS)
# System Preferences → Security & Privacy → Accessibility

# Done! Hebrew-English conversion with Cmd+Shift+H
```

## 🚨 Common Issues

**"Invalid or expired token"**
- Create a new token at https://pypi.org/manage/account/token/
- Make sure you use `__token__` as username (with two underscores)

**"Package already exists"**
- You can't overwrite a published version
- Increment version number and rebuild

**"403 Forbidden"**
- Check token permissions
- Ensure token scope includes the project

## 📊 Post-Publish

After successful publish:

1. **Update GitHub README** if needed
2. **Create a GitHub Release**:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
3. **Share with users!**
