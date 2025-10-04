#!/usr/bin/env python3
"""Install Language Fixer as a macOS LaunchAgent service."""

import os
import sys
import subprocess
import shutil
from pathlib import Path


PLIST_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.languagefixer</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>-m</string>
        <string>language_fixer</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/languagefixer.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/languagefixer.out</string>
</dict>
</plist>
"""


def get_python_path():
    """Get the path to the Python interpreter."""
    return sys.executable


def install_service():
    """Install Language Fixer as a LaunchAgent."""
    print("Installing Language Fixer as a macOS service...")
    print()

    # Get paths
    python_path = get_python_path()
    plist_dest = Path.home() / "Library" / "LaunchAgents" / "com.languagefixer.plist"

    print(f"Python: {python_path}")
    print(f"Service file: {plist_dest}")
    print()

    # Create LaunchAgents directory if it doesn't exist
    plist_dest.parent.mkdir(parents=True, exist_ok=True)

    # Generate plist content
    plist_content = PLIST_TEMPLATE.format(python_path=python_path)

    # Write plist file
    with open(plist_dest, 'w') as f:
        f.write(plist_content)

    print(f"✓ Created service configuration")

    # Unload if already loaded (ignore errors)
    subprocess.run(
        ['launchctl', 'unload', str(plist_dest)],
        capture_output=True
    )

    # Load the LaunchAgent
    result = subprocess.run(
        ['launchctl', 'load', str(plist_dest)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"✗ Error loading service: {result.stderr}")
        return False

    print(f"✓ Service loaded and started")
    print()
    print("=" * 60)
    print("Language Fixer is now running as a background service!")
    print("=" * 60)
    print()
    print("Configuration:")
    print("  - Default: Hebrew-English with Cmd+Shift+H")
    print("  - To customize: Create a config.yaml file")
    print()
    print("Management:")
    print(f"  - Stop:    launchctl unload {plist_dest}")
    print(f"  - Start:   launchctl load {plist_dest}")
    print(f"  - Uninstall: language-fixer-uninstall-service")
    print()
    print("Logs:")
    print("  - Output: tail -f /tmp/languagefixer.out")
    print("  - Errors: tail -f /tmp/languagefixer.err")
    print()

    return True


def uninstall_service():
    """Uninstall Language Fixer service."""
    print("Uninstalling Language Fixer service...")

    plist_file = Path.home() / "Library" / "LaunchAgents" / "com.languagefixer.plist"

    # Stop the service
    if plist_file.exists():
        subprocess.run(
            ['launchctl', 'unload', str(plist_file)],
            capture_output=True
        )
        plist_file.unlink()
        print("✓ Service uninstalled")
    else:
        print("Service not found (already uninstalled)")

    # Remove log files
    for log_file in ['/tmp/languagefixer.out', '/tmp/languagefixer.err']:
        if Path(log_file).exists():
            Path(log_file).unlink()

    print("✓ Log files removed")
    print()
    print("Language Fixer service has been uninstalled.")


def main():
    """Entry point for service installation."""
    if sys.platform != 'darwin':
        print("Error: Service installation is only supported on macOS")
        sys.exit(1)

    try:
        if not install_service():
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main_uninstall():
    """Entry point for service uninstallation."""
    if sys.platform != 'darwin':
        print("Error: Service uninstallation is only supported on macOS")
        sys.exit(1)

    try:
        uninstall_service()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
