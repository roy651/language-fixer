"""Command-line interface for language-fixer."""

import sys
import os
import argparse
from pathlib import Path
import shutil
import json

from . import __version__
from .listener import LanguageFixer
from .config import load_config, get_default_config
from .generate_mapping import main as generate_mapping_main
from .install_service import (
    main as install_main,
    main_uninstall as uninstall_main,
    main_restart as restart_main,
    main_stop as stop_main,
    main_status as status_main
)


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    config_dir = Path.home() / ".config" / "language-fixer"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_package_data_dir() -> Path:
    """Get the package data directory containing mappings."""
    # Try package-installed location first
    package_mappings = Path(__file__).parent / "mappings"
    if package_mappings.exists():
        return package_mappings

    # Fall back to source tree location (for development)
    source_mappings = Path(__file__).parent.parent.parent / "mappings"
    if source_mappings.exists():
        return source_mappings

    raise FileNotFoundError("Could not find mappings directory")


def cmd_init(args):
    """Initialize configuration in user's home directory."""
    config_dir = get_config_dir()
    config_file = config_dir / "config.yaml"
    mappings_dir = config_dir / "mappings"

    # Copy mappings
    package_mappings = get_package_data_dir()
    if package_mappings.exists():
        shutil.copytree(package_mappings, mappings_dir, dirs_exist_ok=True)
        print(f"✓ Copied language mappings to {mappings_dir}")

    # Create default config if it doesn't exist
    if config_file.exists() and not args.force:
        print(f"Config already exists at {config_file}")
        print("Use --force to overwrite")
        return

    # Create default config
    default_config = """# Language Fixer Configuration
buffer_timeout: 10.0

language_pairs:
  - name: "Hebrew-English"
    mapping_file: "~/.config/language-fixer/mappings/hebrew-english.json"
    hotkey: "cmd+alt+h"
    enabled: true
"""

    config_file.write_text(default_config)
    print(f"✓ Created config at {config_file}")
    print()
    print("To add more languages, edit the config file:")
    print(f"  {config_file}")
    print()
    print("Available mappings:")
    for mapping_file in mappings_dir.glob("*.json"):
        with open(mapping_file) as f:
            data = json.load(f)
            print(f"  - {data.get('name', mapping_file.stem)}: {mapping_file.name}")


def cmd_config(args):
    """Show or edit configuration."""
    config_dir = get_config_dir()
    config_file = config_dir / "config.yaml"

    if args.path:
        print(config_file)
        return

    if not config_file.exists():
        print("No config found. Run 'lang-fix init' first.")
        sys.exit(1)

    if args.edit:
        import subprocess
        editor = os.environ.get('EDITOR', 'nano')
        subprocess.run([editor, str(config_file)])
    else:
        print(config_file.read_text())


def cmd_mapping(args):
    """Manage language mappings."""
    if args.action == 'list':
        config_dir = get_config_dir()
        mappings_dir = config_dir / "mappings"

        if not mappings_dir.exists():
            print("No mappings found. Run 'lang-fix init' first.")
            return

        print("Available mappings:")
        for mapping_file in sorted(mappings_dir.glob("*.json")):
            with open(mapping_file) as f:
                data = json.load(f)
                name = data.get('name', mapping_file.stem)
                desc = data.get('description', '')
                print(f"  {name}")
                if desc:
                    print(f"    {desc}")
                print(f"    File: {mapping_file.name}")
                print()

    elif args.action == 'create':
        # Use the existing generate mapping tool
        generate_mapping_main()


def cmd_doctor(args):
    """Diagnose installation and permissions."""
    import subprocess

    print("=== Language Fixer Diagnostics ===\n")

    # Show Python path (resolved)
    python_path = sys.executable
    real_python_path = os.path.realpath(sys.executable)

    print(f"Python executable: {python_path}")
    if python_path != real_python_path:
        print(f"  (symlink to: {real_python_path})")
    print(f"\n  → Add THIS path to both Input Monitoring AND Accessibility:")
    print(f"     {real_python_path}\n")

    # Check config
    config_dir = get_config_dir()
    config_file = config_dir / "config.yaml"
    if config_file.exists():
        print(f"✓ Config found: {config_file}")
    else:
        print(f"✗ Config not found. Run: lang-fix init")
        return

    # Check mappings
    mappings_dir = config_dir / "mappings"
    if mappings_dir.exists():
        mapping_count = len(list(mappings_dir.glob("*.json")))
        print(f"✓ Found {mapping_count} language mappings")
    else:
        print(f"✗ Mappings not found")

    # Check service
    plist_file = Path.home() / "Library" / "LaunchAgents" / "com.languagefixer.plist"
    if plist_file.exists():
        print(f"✓ Service installed: {plist_file}")

        # Check if running
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True
        )
        if "com.languagefixer" in result.stdout:
            print("✓ Service is running")
        else:
            print("✗ Service not running. Try: lang-fix service restart")
    else:
        print(f"✗ Service not installed. Run: lang-fix service install")

    # Permission instructions
    print("\n=== Required Permissions ===")
    print("You must add the Python path to BOTH:")
    print("1. System Preferences → Security & Privacy → Input Monitoring")
    print("2. System Preferences → Security & Privacy → Accessibility")
    print(f"\nPath to add: {real_python_path}")
    print("\nAfter granting permissions, restart the service:")
    print("  lang-fix service restart")


def cmd_service(args):
    """Manage background service."""
    if args.action == 'install':
        install_main()
        # Show permission reminder
        real_path = os.path.realpath(sys.executable)
        print("\n=== IMPORTANT: Grant Permissions ===")
        print(f"Add this Python path to both Input Monitoring AND Accessibility:")
        print(f"  {real_path}")
        print("\nThen run: lang-fix service restart")
    elif args.action == 'uninstall':
        uninstall_main()
    elif args.action == 'restart':
        restart_main()
    elif args.action == 'stop':
        stop_main()
    elif args.action == 'status':
        status_main()


def cmd_run(args):
    """Run the language fixer (foreground)."""
    config_dir = get_config_dir()
    config_file = config_dir / "config.yaml"

    if config_file.exists():
        # Update sys.path to find config
        import os
        os.chdir(config_dir)
        try:
            config = load_config()
            print(f"✓ Loaded config from {config_file}")
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Using default configuration")
            config = get_default_config()
    else:
        print("No config found. Using default Hebrew-English configuration.")
        print("Run 'lang-fix init' to customize.")
        config = get_default_config()

    print("Language Fixer is running. Press Ctrl+C to stop.")
    fixer = LanguageFixer(config=config)
    fixer.start()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='lang-fix',
        description='Language Fixer - Fix text typed in wrong keyboard layout',
        epilog='Run "lang-fix <command> --help" for more information on a command.'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # init command
    init_parser = subparsers.add_parser('init', help='Initialize configuration')
    init_parser.add_argument('--force', action='store_true', help='Overwrite existing config')
    init_parser.set_defaults(func=cmd_init)

    # config command
    config_parser = subparsers.add_parser('config', help='View or edit configuration')
    config_parser.add_argument('--path', action='store_true', help='Show config file path')
    config_parser.add_argument('--edit', action='store_true', help='Edit config file')
    config_parser.set_defaults(func=cmd_config)

    # mapping command
    mapping_parser = subparsers.add_parser('mapping', help='Manage language mappings')
    mapping_parser.add_argument('action', choices=['list', 'create'], help='Action to perform')
    mapping_parser.set_defaults(func=cmd_mapping)

    # doctor command
    doctor_parser = subparsers.add_parser('doctor', help='Diagnose installation and permissions')
    doctor_parser.set_defaults(func=cmd_doctor)

    # service command
    service_parser = subparsers.add_parser('service', help='Manage background service')
    service_parser.add_argument('action', choices=['install', 'uninstall', 'restart', 'stop', 'status'],
                               help='Service action')
    service_parser.set_defaults(func=cmd_service)

    # run command (default)
    run_parser = subparsers.add_parser('run', help='Run language fixer (foreground)')
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
