#!/bin/bash
set -e

# Language Fixer Installation Script
# This script sets up the LaunchAgent to run Language Fixer automatically

echo "Installing Language Fixer LaunchAgent..."

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Find uv executable
UV_PATH=$(which uv)
if [ -z "$UV_PATH" ]; then
    echo "Error: uv not found in PATH"
    echo "Please install uv first: https://github.com/astral-sh/uv"
    exit 1
fi

echo "Found uv at: $UV_PATH"
echo "Project directory: $PROJECT_DIR"

# Create the plist file from template
PLIST_TEMPLATE="$PROJECT_DIR/com.languagefixer.plist.template"
PLIST_DEST="$HOME/Library/LaunchAgents/com.languagefixer.plist"

if [ ! -f "$PLIST_TEMPLATE" ]; then
    echo "Error: Template file not found: $PLIST_TEMPLATE"
    exit 1
fi

# Replace placeholders in template
sed -e "s|{{UV_PATH}}|$UV_PATH|g" \
    -e "s|{{PROJECT_DIR}}|$PROJECT_DIR|g" \
    "$PLIST_TEMPLATE" > "$PLIST_DEST"

echo "Created plist file: $PLIST_DEST"

# Unload if already loaded (ignore errors if not loaded)
launchctl unload "$PLIST_DEST" 2>/dev/null || true

# Load the LaunchAgent
launchctl load "$PLIST_DEST"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Language Fixer is now running in the background."
echo ""
echo "Usage:"
echo "  - Press Cmd+Shift+H to convert text between Hebrew and English"
echo ""
echo "Management:"
echo "  - Stop:  launchctl unload ~/Library/LaunchAgents/com.languagefixer.plist"
echo "  - Start: launchctl load ~/Library/LaunchAgents/com.languagefixer.plist"
echo "  - Logs:  tail -f /tmp/languagefixer.out"
echo "  - Errors: tail -f /tmp/languagefixer.err"
echo ""
