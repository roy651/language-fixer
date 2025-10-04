#!/bin/bash
set -e

# Language Fixer Restart Script

echo "Restarting Language Fixer..."

PLIST_FILE="$HOME/Library/LaunchAgents/com.languagefixer.plist"

if [ ! -f "$PLIST_FILE" ]; then
    echo "Error: Language Fixer is not installed as a service"
    echo "Run ./scripts/install.sh first"
    exit 1
fi

# Stop the service
echo "Stopping service..."
launchctl unload "$PLIST_FILE" 2>/dev/null || true
sleep 1

# Start the service
echo "Starting service..."
launchctl load "$PLIST_FILE"

echo ""
echo "✓ Language Fixer restarted successfully!"
echo ""
echo "To view logs:"
echo "  ./scripts/view_logs.sh"
echo ""
