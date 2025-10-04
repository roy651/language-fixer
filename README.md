# Language Fixer

A flexible macOS utility that retroactively fixes text typed in the wrong keyboard layout. Supports multiple language pairs with configurable hotkeys.

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

### Recommended: Install with pipx

`pipx` is the cleanest way to install Python CLI tools:

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Close and reopen your terminal, then:
pipx install language-fixer
```

### Alternative: Install with pip

```bash
pip3 install language-fixer
```

**Note:** If you use pip, you may need to add Python's bin directory to your PATH:
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```
Add this to your `~/.zshrc` or `~/.bash_profile` to make it permanent.

### Setup as Background Service

```bash
language-fixer-install-service
```

### Grant Permissions (Important!)

macOS requires **TWO permissions** for the keyboard listener to work:

**1. Input Monitoring** (will prompt automatically when first run)
   - System Preferences → Security & Privacy → **Input Monitoring**
   - Enable: **Python** (or python3)

**2. Accessibility** (must enable manually)
   - System Preferences → Security & Privacy → **Accessibility**
   - Click lock to make changes
   - Click **+** and navigate to `/usr/bin` or `/usr/local/bin`
   - Add **python3**
   - Enable the checkbox

**After granting both permissions:**
```bash
language-fixer-restart-service
```

### Service Management

```bash
language-fixer-status              # Check if running
language-fixer-restart-service     # Restart service
language-fixer-stop-service        # Stop service
language-fixer-uninstall-service   # Uninstall completely
```

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

### Default Mode (Hebrew-English)

```bash
uv run python -m language_fixer
```

Press `Cmd+Shift+H` to convert between Hebrew and English.

### With Configuration

1. **Copy the example config**:
   ```bash
   cp config.example.yaml config.yaml
   ```

2. **Edit config.yaml** to enable/disable language pairs and customize hotkeys

3. **Run**:
   ```bash
   uv run python -m language_fixer
   ```

## Configuration

Create a `config.yaml` file in the project root to customize behavior:

```yaml
# Buffer timeout in seconds
buffer_timeout: 10.0

# Language pairs
language_pairs:
  - name: "Hebrew-English"
    mapping_file: "mappings/hebrew-english.json"
    hotkey: "cmd+shift+h"
    enabled: true

  - name: "Arabic-English"
    mapping_file: "mappings/arabic-english.json"
    hotkey: "cmd+shift+a"
    enabled: true

  - name: "Russian-English"
    mapping_file: "mappings/russian-english.json"
    hotkey: "cmd+shift+r"
    enabled: true
```

### Built-in Language Mappings

- **Hebrew-English**: `mappings/hebrew-english.json`
- **Arabic-English**: `mappings/arabic-english.json`
- **Russian-English**: `mappings/russian-english.json`

## Creating Custom Language Mappings

Use the built-in mapping generator:

```bash
uv run language-fixer-generate-mapping
```

The tool will:
1. Ask for language pair details
2. Guide you through mapping each key
3. Save the mapping file in the `mappings/` directory
4. Show you how to add it to your config

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

## Running as Background Service

To have Language Fixer start automatically when you log in, use the provided management scripts:

### Install as Service
```bash
./scripts/install.sh
```

### Management Commands
```bash
# Check if running
./scripts/is_running.sh

# View logs
./scripts/view_logs.sh
./scripts/view_logs.sh -f    # Follow logs in real-time

# Restart service
./scripts/restart.sh

# Uninstall service
./scripts/uninstall.sh
```

### Manual Service Control
```bash
# Stop the service
launchctl unload ~/Library/LaunchAgents/com.languagefixer.plist

# Start the service
launchctl load ~/Library/LaunchAgents/com.languagefixer.plist
```

## How It Works

Language Fixer monitors your keyboard input and maintains a buffer of recently typed characters. When you press a hotkey:

1. Detects the source language of the buffered text
2. Maps each character to its equivalent on the target keyboard layout
3. Deletes the original text
4. Pastes the converted text

The conversion is based on physical keyboard positions, so each key maps to its equivalent character in the other language.

## Uninstallation

1. **Stop and remove the LaunchAgent** (if installed):
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.languagefixer.plist
   rm ~/Library/LaunchAgents/com.languagefixer.plist
   ```

2. **Remove the project**:
   ```bash
   cd ..
   rm -rf language-fixer
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
│   ├── __main__.py           # Entry point
│   ├── config.py             # Configuration management
│   ├── converter.py          # Text conversion logic
│   ├── listener.py           # Keyboard listener
│   └── generate_mapping.py   # Mapping generator tool
├── mappings/
│   ├── hebrew-english.json
│   ├── arabic-english.json
│   └── russian-english.json
├── scripts/
│   ├── install.sh            # Install as service
│   ├── uninstall.sh          # Uninstall service
│   ├── restart.sh            # Restart service
│   ├── is_running.sh         # Check status
│   └── view_logs.sh          # View logs
├── tests/
│   └── test_converter.py
├── config.example.yaml
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
