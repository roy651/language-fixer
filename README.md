# Language Fixer

A flexible macOS utility that retroactively fixes text typed in the wrong keyboard layout. Supports multiple language pairs with configurable hotkeys.

<p align="center">
  https://github.com/user-attachments/assets/8c7ab90d-cf3f-4473-849a-c14cefea8278
</p>

## Features

- **Multiple Language Support**: Hebrew, Arabic, Russian, or create your own
- **Configurable Hotkeys**: Each language pair can have its own hotkey
- **Toggle-Back**: Press hotkey again to revert the conversion
- **Smart Detection**: Automatically detects the source language
- **Seamless Integration**: Runs quietly in the background
- **Configurable Buffer**: Adjust how long typed text is remembered
- **RTL Support**: Properly handles right-to-left text

## Requirements

- macOS (tested on macOS 10.14+)
- Python 3.9+

## Installation

### Option 1: Install with pipx (Recommended)

`pipx` is the cleanest way to install Python CLI tools:

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Close and reopen your terminal, then:
pipx install language-fixer

# Initialize configuration
lang-fix init

# Install as background service
lang-fix service install
```

### Option 2: Install with pip

```bash
pip3 install language-fixer

# Initialize configuration
lang-fix init

# Install as background service
lang-fix service install
```

**Note:** If you use pip, you may need to add Python's bin directory to your PATH:
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```
Add this to your `~/.zshrc` or `~/.bash_profile` to make it permanent.

### Grant Permissions (Important!)

macOS requires **TWO permissions** for the keyboard listener to work.

**First, find the exact Python path to grant permissions to:**
```bash
lang-fix doctor
```

This shows the exact Python executable path (e.g., `/opt/homebrew/bin/python3` for pipx installations).

**Then grant permissions:**

**1. Input Monitoring** (will prompt automatically when first run)
   - System Preferences → Security & Privacy → **Input Monitoring**
   - Add the Python path shown by `lang-fix doctor`

**2. Accessibility** (must enable manually)
   - System Preferences → Security & Privacy → **Accessibility**
   - Click lock to make changes
   - Click **+** and navigate to the Python path
   - Add the executable and enable the checkbox

**After granting both permissions, restart the service:**
```bash
lang-fix service restart
```

**Troubleshooting:** If conversion doesn't work, run `lang-fix doctor` to verify the correct Python path is granted permissions.

### Option 2: Install from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/language-fixer.git
   cd language-fixer
   ```

2. **Install with uv**:
   ```bash
   uv sync
   ```

3. **Grant accessibility permissions** (same as above)

4. **Install as service** (optional):
   ```bash
   ./scripts/install.sh
   ```

## Quick Start

After installation, initialize the configuration:

```bash
lang-fix init
```

This creates config and mappings in `~/.config/language-fixer/` with Hebrew-English support by default.

Then install as a service:

```bash
lang-fix service install
```

Grant permissions (see Permissions section above), restart, and you're done!

```bash
lang-fix service restart
```

Type in the wrong language and press `Cmd+Shift+H` to fix!

## CLI Commands

Language Fixer provides both `lang-fix` (short) and `language-fixer` (long) commands:

### Setup Commands

```bash
# Initialize configuration (first time setup)
lang-fix init

# Diagnose installation and show permission instructions
lang-fix doctor

# View available mappings
lang-fix mapping list

# Create custom language mapping
lang-fix mapping create

# View config file
lang-fix config

# Edit config file
lang-fix config --edit

# Show config file path
lang-fix config --path
```

### Service Management

```bash
# Install as background service
lang-fix service install

# Check service status
lang-fix service status

# Restart service (after config changes or granting permissions)
lang-fix service restart

# Stop service
lang-fix service stop

# Uninstall service
lang-fix service uninstall
```

### Run Manually

```bash
# Run in foreground (for testing)
lang-fix run
```

## Configuration

Language Fixer stores configuration in `~/.config/language-fixer/`:

- `config.yaml` - Main configuration file
- `mappings/` - Language mapping files

### Default Configuration

After running `lang-fix init`, you get Hebrew-English support:

```yaml
buffer_timeout: 10.0

language_pairs:
  - name: "Hebrew-English"
    mapping_file: "~/.config/language-fixer/mappings/hebrew-english.json"
    hotkey: "cmd+shift+h"
    enabled: true
```

### Adding More Languages

Edit `~/.config/language-fixer/config.yaml`:

```yaml
buffer_timeout: 10.0

language_pairs:
  - name: "Hebrew-English"
    mapping_file: "~/.config/language-fixer/mappings/hebrew-english.json"
    hotkey: "cmd+shift+h"
    enabled: true

  - name: "Arabic-English"
    mapping_file: "~/.config/language-fixer/mappings/arabic-english.json"
    hotkey: "cmd+shift+a"
    enabled: true

  - name: "Russian-English"
    mapping_file: "~/.config/language-fixer/mappings/russian-english.json"
    hotkey: "cmd+shift+r"
    enabled: true
```

### Create Custom Mapping

```bash
lang-fix mapping create
```

This will:
1. Ask for language pair details (e.g., "Spanish-English")
2. Guide you through mapping each keyboard key
3. Save to `~/.config/language-fixer/mappings/your-language.json`
4. Show you how to add it to config

All languages work exactly the same way!

## Usage Examples

### Basic Usage

1. Type text in wrong language: `akuo` (meant to type שלום)
2. Press `Cmd+Shift+H`
3. Text converts to: `שלום`

### Toggle Back

1. Type: `hello` → Press `Cmd+Shift+H` → Converts to: `יקךךם`
2. Press `Cmd+Shift+H` again (immediately) → Reverts to: `hello`

### Multiple Languages

With config enabled for multiple languages:
- `Cmd+Shift+H` for Hebrew-English
- `Cmd+Shift+A` for Arabic-English
- `Cmd+Shift+R` for Russian-English

## Viewing Logs

If you need to troubleshoot:

```bash
# View error logs
tail -f /tmp/languagefixer.err

# View output logs
tail -f /tmp/languagefixer.out
```

## How It Works

Language Fixer monitors your keyboard input and maintains a buffer of recently typed characters. When you press a hotkey:

1. Detects the source language of the buffered text
2. Maps each character to its equivalent on the target keyboard layout
3. Deletes the original text
4. Pastes the converted text

The conversion is based on physical keyboard positions, so each key maps to its equivalent character in the other language.

## Uninstallation

**For pipx installation:**
```bash
lang-fix service uninstall
pipx uninstall language-fixer
```

**For pip installation:**
```bash
lang-fix service uninstall
pip3 uninstall language-fixer
```

**Remove configuration** (optional):
```bash
rm -rf ~/.config/language-fixer
```

## Development

### Running tests

```bash
uv run pytest
```

### Project structure

```
language-fixer/
├── src/language_fixer/
│   ├── __init__.py
│   ├── cli.py                # Main CLI interface
│   ├── config.py             # Configuration management
│   ├── converter.py          # Text conversion logic
│   ├── listener.py           # Keyboard listener
│   ├── generate_mapping.py   # Mapping generator tool
│   └── install_service.py    # Service installation
├── mappings/
│   ├── hebrew-english.json
│   ├── arabic-english.json
│   └── russian-english.json
├── tests/
│   ├── test_converter.py
│   └── test_listener.py
├── scripts/                  # Legacy scripts for source installation
├── pyproject.toml
└── README.md
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Troubleshooting

**The hotkey doesn't work:**
- Make sure you've granted Accessibility permissions to your terminal app
- Try restarting the application
- Check that your hotkey doesn't conflict with other apps

**Text isn't converting correctly:**
- The buffer has a timeout (default 10 seconds) - press the hotkey within this window
- The converter works on buffered text only - if you've pressed Enter, Tab, or arrow keys, the buffer is cleared

**Service won't start:**
- Check the error logs: `cat /tmp/languagefixer.err`
- Make sure uv is installed and in your PATH
- Verify the paths in `~/Library/LaunchAgents/com.languagefixer.plist` are correct

**Config file errors:**
- Make sure PyYAML is installed: `uv sync`
- Check your config.yaml syntax is valid YAML
- Verify mapping file paths are correct and files exist

**Custom mapping not working:**
- Ensure the mapping file is valid JSON
- Check that the mapping file path in config.yaml is correct
- Make sure the language pair is enabled in config

## Contributing

Contributions are welcome! Feel free to:
- Add new language mappings
- Report bugs
- Suggest features
- Submit pull requests

## Roadmap

Future improvements:
- Visual feedback when conversion happens
- App-specific exclusions
- Smart word boundary detection
- Additional platform support
