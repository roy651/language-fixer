#!/bin/bash

# Check if Language Fixer is running

if launchctl list | grep -q "com.languagefixer"; then
    echo "✓ Language Fixer is RUNNING"
    echo ""
    launchctl list | grep com.languagefixer | awk '{print "  PID: " $1 "\n  Status: " $2 "\n  Label: " $3}'
    echo ""

    # Show recent activity from logs
    if [ -f "/tmp/languagefixer.out" ]; then
        echo "Recent output (last 5 lines):"
        tail -5 /tmp/languagefixer.out | sed 's/^/  /'
    fi

    exit 0
else
    echo "✗ Language Fixer is NOT RUNNING"
    echo ""
    echo "To start it:"
    echo "  ./scripts/install.sh    (install as service)"
    echo "  uv run python -m language_fixer    (run manually)"
    echo ""
    exit 1
fi
