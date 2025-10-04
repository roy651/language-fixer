#!/bin/bash
set -e

# Language Fixer Uninstallation Script

echo "Uninstalling Language Fixer..."

PLIST_FILE="$HOME/Library/LaunchAgents/com.languagefixer.plist"

# Check if service is running and stop it
if launchctl list | grep -q "com.languagefixer"; then
    echo "Stopping Language Fixer service..."
    launchctl unload "$PLIST_FILE" 2>/dev/null || true
    echo "✓ Service stopped"
fi

# Remove plist file
if [ -f "$PLIST_FILE" ]; then
    echo "Removing LaunchAgent configuration..."
    rm "$PLIST_FILE"
    echo "✓ LaunchAgent removed"
else
    echo "LaunchAgent not found (already removed or not installed)"
fi

# Remove log files
if [ -f "/tmp/languagefixer.out" ] || [ -f "/tmp/languagefixer.err" ]; then
    echo "Removing log files..."
    rm -f /tmp/languagefixer.out /tmp/languagefixer.err
    echo "✓ Log files removed"
fi

echo ""
echo "✓ Language Fixer uninstalled successfully!"
echo ""
echo "Note: The project directory has not been removed."
echo "To completely remove Language Fixer, delete this directory:"
echo "  cd .. && rm -rf language-fixer"
echo ""
