#!/bin/bash
set -e

# Build script for Language Fixer package

echo "Building Language Fixer package..."
echo ""

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info

# Build the package
echo "Building wheel and source distribution..."
if command -v python3 &> /dev/null; then
    python3 -m build
elif command -v uv &> /dev/null; then
    uv run python -m build
else
    echo "Error: Neither python3 nor uv found"
    exit 1
fi

echo ""
echo "✓ Build complete!"
echo ""

# Show what was built
ls -lh dist/

echo ""
echo "To verify the build:"
echo "  python3 -m twine check dist/*"
echo "  # OR"
echo "  uv run twine check dist/*"
echo ""
echo "To upload to PyPI:"
echo "  python3 -m twine upload dist/*"
echo "  # OR"
echo "  uv run twine upload dist/*"
echo ""
