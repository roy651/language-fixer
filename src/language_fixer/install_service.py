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
    """Get the path to the Python interpreter (venv path, not resolved)."""
    # Use the venv Python path as-is for running the service
    # Don't resolve symlinks here - we need the venv Python, not system Python
    return sys.executable


def get_plist_path():
    """Get the plist file path."""
    return Path.home() / "Library" / "LaunchAgents" / "com.languagefixer.plist"


def is_service_running():
    """Check if the service is currently running."""
    result = subprocess.run(
        ['launchctl', 'list'],
        capture_output=True,
        text=True
    )
    return 'com.languagefixer' in result.stdout


def install_service():
    """Install Language Fixer as a LaunchAgent."""
    print("Installing Language Fixer as a macOS service...")
    print()

    # Get paths
    python_path = get_python_path()
    plist_dest = get_plist_path()

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
    print("=" * 70)
    print("Language Fixer is now running as a background service!")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT: Grant Permissions")
    print()
    print("macOS needs TWO permissions for the keyboard listener:")
    print()

    # Show the real Python path for permissions
    real_python_path = os.path.realpath(python_path)
    print("Add this Python executable to BOTH permission lists:")
    print(f"  {real_python_path}")
    print()

    print("1. Input Monitoring:")
    print("   System Settings → Privacy & Security → Input Monitoring")
    print(f"   ✓ Enable: {real_python_path}")
    print()
    print("2. Accessibility:")
    print("   System Settings → Privacy & Security → Accessibility")
    print(f"   ✓ Enable: {real_python_path}")
    print()
    print("After granting BOTH permissions, restart the service:")
    print("  lang-fix service restart")
    print()
    print("=" * 70)
    print()
    print("Management Commands:")
    print("  language-fixer-status           - Check if running")
    print("  language-fixer-restart-service  - Restart the service")
    print("  language-fixer-stop-service     - Stop the service")
    print("  language-fixer-uninstall-service - Uninstall completely")
    print()
    print("Default Hotkey: Cmd+Option+H (Hebrew-English)")
    print("Customize: Create a config.yaml file")
    print()
    print("Logs:")
    print("  tail -f /tmp/languagefixer.out")
    print("  tail -f /tmp/languagefixer.err")
    print()

    return True


def uninstall_service():
    """Uninstall Language Fixer service."""
    print("Uninstalling Language Fixer service...")

    plist_file = get_plist_path()

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


def restart_service():
    """Restart the Language Fixer service."""
    print("Restarting Language Fixer service...")

    plist_file = get_plist_path()

    if not plist_file.exists():
        print("✗ Service not installed. Run: language-fixer-install-service")
        return False

    # Stop
    subprocess.run(
        ['launchctl', 'unload', str(plist_file)],
        capture_output=True
    )
    print("✓ Service stopped")

    # Start
    result = subprocess.run(
        ['launchctl', 'load', str(plist_file)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"✗ Error starting service: {result.stderr}")
        return False

    print("✓ Service started")
    print()
    print("Service restarted successfully!")
    return True


def stop_service():
    """Stop the Language Fixer service."""
    print("Stopping Language Fixer service...")

    plist_file = get_plist_path()

    if not plist_file.exists():
        print("✗ Service not installed")
        return False

    subprocess.run(
        ['launchctl', 'unload', str(plist_file)],
        capture_output=True
    )

    print("✓ Service stopped")
    print()
    print("To start again: language-fixer-restart-service")
    return True


def status_service():
    """Check and display service status."""
    plist_file = get_plist_path()

    print("Language Fixer Service Status")
    print("=" * 40)
    print()

    if not plist_file.exists():
        print("Status: NOT INSTALLED")
        print()
        print("To install: language-fixer-install-service")
        return

    if is_service_running():
        print("Status: RUNNING ✓")
        print()

        # Show recent logs if available
        log_file = Path('/tmp/languagefixer.out')
        if log_file.exists() and log_file.stat().st_size > 0:
            print("Recent output:")
            result = subprocess.run(
                ['tail', '-5', str(log_file)],
                capture_output=True,
                text=True
            )
            for line in result.stdout.strip().split('\n'):
                print(f"  {line}")
        print()
        print("Commands:")
        print("  language-fixer-restart-service  - Restart")
        print("  language-fixer-stop-service     - Stop")
    else:
        print("Status: STOPPED")
        print()
        print("To start: language-fixer-restart-service")


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


def main_restart():
    """Entry point for service restart."""
    if sys.platform != 'darwin':
        print("Error: Service management is only supported on macOS")
        sys.exit(1)

    try:
        if not restart_service():
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main_stop():
    """Entry point for service stop."""
    if sys.platform != 'darwin':
        print("Error: Service management is only supported on macOS")
        sys.exit(1)

    try:
        if not stop_service():
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main_status():
    """Entry point for service status check."""
    if sys.platform != 'darwin':
        print("Error: Service management is only supported on macOS")
        sys.exit(1)

    try:
        status_service()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
