#!/bin/bash

# View Language Fixer logs

echo "Language Fixer Logs"
echo "==================="
echo ""

# Check if service is running
if ! launchctl list | grep -q "com.languagefixer"; then
    echo "⚠ Warning: Language Fixer service is not running"
    echo ""
fi

# Function to show log file
show_log() {
    local file=$1
    local name=$2

    if [ -f "$file" ]; then
        echo "=== $name ==="
        if [ -s "$file" ]; then
            tail -20 "$file"
        else
            echo "(empty)"
        fi
        echo ""
    else
        echo "=== $name ==="
        echo "(not found)"
        echo ""
    fi
}

# Show last 20 lines of each log
show_log "/tmp/languagefixer.out" "Standard Output"
show_log "/tmp/languagefixer.err" "Error Output"

echo "To follow logs in real-time:"
echo "  tail -f /tmp/languagefixer.out"
echo "  tail -f /tmp/languagefixer.err"
echo ""

# Offer to tail if requested
if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
    echo "Following standard output (Ctrl+C to stop)..."
    tail -f /tmp/languagefixer.out
fi
