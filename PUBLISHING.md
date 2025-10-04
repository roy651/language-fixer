# Publishing Language Fixer to PyPI

This guide explains how to publish Language Fixer to PyPI so users can install it with a single command.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [Test PyPI](https://test.pypi.org/account/register/) (for testing)
   - [PyPI](https://pypi.org/account/register/) (for production)

2. **API Tokens**: Create API tokens for uploading:
   - [Test PyPI Token](https://test.pypi.org/manage/account/token/)
   - [PyPI Token](https://pypi.org/manage/account/token/)

3. **Install build tools**:
   ```bash
   uv pip install build twine
   ```

## Publishing Steps

### 1. Update Version

Update version in `pyproject.toml` and `src/language_fixer/__init__.py`:

```python
__version__ = "0.2.0"  # Increment as needed
```

### 2. Update URLs

In `pyproject.toml`, update the GitHub URLs:

```toml
[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/language-fixer"
Issues = "https://github.com/YOUR_USERNAME/language-fixer/issues"
```

### 3. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and source distribution (use one of these):
python3 -m build          # If you have python3
# OR
uv run python -m build    # If using uv
```

This creates:
- `dist/language_fixer-0.2.0-py3-none-any.whl` (wheel)
- `dist/language-fixer-0.2.0.tar.gz` (source)

### 4. Test on Test PyPI (Recommended)

```bash
# Upload to Test PyPI
python3 -m twine upload --repository testpypi dist/*
# OR
uv run twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ language-fixer
```

### 5. Publish to PyPI

```bash
# Upload to PyPI
python3 -m twine upload dist/*
# OR
uv run twine upload dist/*
```

You'll be prompted for your API token.

## After Publishing

Users can now install with:

```bash
pip install language-fixer
```

Or with uv:

```bash
uv pip install language-fixer
```

## One-Command Installation (User Experience)

### Via pipx (Recommended for CLI tools)

```bash
pipx install language-fixer
language-fixer  # Run directly
```

### Via pip in isolated environment

```bash
# Create virtual environment and install
python -m venv ~/.language-fixer-env
~/.language-fixer-env/bin/pip install language-fixer
~/.language-fixer-env/bin/language-fixer
```

### Via uv (Modern, fast)

```bash
uv tool install language-fixer
language-fixer
```

## Setup Script for Users

Create an install script users can run:

```bash
# Quick install via pipx (recommended)
pipx install language-fixer

# Or via uv
uv tool install language-fixer

# Or via pip
pip install language-fixer
```

Then setup as service (macOS):

```bash
# Get the package location
PACKAGE_DIR=$(python -c "import language_fixer; import os; print(os.path.dirname(language_fixer.__file__))")

# Copy and run install script (you'll need to include this in the package)
```

## Including Installation Scripts in Package

To make scripts available after pip install, update `pyproject.toml`:

```toml
[project.scripts]
language-fixer = "language_fixer.__main__:main"
language-fixer-generate-mapping = "language_fixer.generate_mapping:main"
language-fixer-install-service = "language_fixer.install_service:main"  # New
```

Then create `src/language_fixer/install_service.py` to handle service installation programmatically.

## Version Management

### Semantic Versioning
- `0.2.0` → `0.2.1`: Bug fixes
- `0.2.0` → `0.3.0`: New features (backward compatible)
- `0.2.0` → `1.0.0`: Major changes (breaking)

### Release Checklist

- [ ] Update version in `__init__.py` and `pyproject.toml`
- [ ] Update CHANGELOG (if you create one)
- [ ] Run tests: `uv run pytest`
- [ ] Build package: `python -m build`
- [ ] Test on Test PyPI
- [ ] Upload to PyPI
- [ ] Create GitHub release tag
- [ ] Update README if needed

## Automation with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Add `PYPI_API_TOKEN` to GitHub repository secrets.

## User Installation Flow (Final)

After publishing to PyPI, users can install with ONE command:

### Simple Installation
```bash
pipx install language-fixer
```

### Run
```bash
language-fixer  # Start the fixer
```

### Service Setup (macOS)
We can add a post-install command:
```bash
language-fixer-setup-service  # Install as background service
```

This would be a new Python script in the package that handles the LaunchAgent setup.
