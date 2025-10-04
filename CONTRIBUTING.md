# Contributing to Language Fixer

Thanks for your interest in contributing! This guide will help you get started.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/roy651/language-fixer.git
   cd language-fixer
   ```

2. **Install dependencies**
   ```bash
   pip install uv
   uv sync
   ```

3. **Run tests**
   ```bash
   uv run pytest
   ```

## Project Structure

- `src/language_fixer/` - Main source code
  - `converter.py` - Text conversion logic
  - `listener.py` - Keyboard event handling
  - `config.py` - Configuration management
  - `install_service.py` - macOS service management
- `mappings/` - Language mapping files (JSON)
- `tests/` - Test files
- `scripts/` - Shell scripts for service management

## Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   uv run pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Adding New Language Mappings

To add support for a new language:

1. Create a JSON mapping file in `mappings/` directory
2. Use the mapping generator tool:
   ```bash
   language-fixer-generate-mapping
   ```
3. Test the mapping thoroughly
4. Submit a pull request with the new mapping file

## Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Keep functions focused and concise
- Add docstrings for public functions

## Reporting Issues

- Check existing issues first
- Provide clear reproduction steps
- Include your macOS version and Python version
- Share relevant error messages or logs

## Questions?

Open an issue for discussion or questions about contributing.
