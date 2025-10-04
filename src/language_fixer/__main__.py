"""Main entry point for language-fixer."""

import sys
from pathlib import Path
from .listener import LanguageFixer
from .config import load_config, get_default_config


def main():
    """Run the language fixer."""
    try:
        # Try to load config from user's config directory first
        config_dir = Path.home() / ".config" / "language-fixer"
        config_file = config_dir / "config.yaml"

        if config_file.exists():
            config = load_config(str(config_file))
            print(f"Loaded configuration from {config_file}")
        else:
            # Try current directory
            config = load_config()
            print(f"Loaded configuration from config.yaml")
    except FileNotFoundError:
        # No config file, use defaults
        print("No config.yaml found, using default configuration")
        config = get_default_config()
    except ImportError as e:
        print(f"Warning: {e}")
        print("Falling back to default configuration without config file support")
        config = get_default_config()
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        print("Falling back to default configuration")
        config = get_default_config()

    fixer = LanguageFixer(config=config)
    fixer.start()


if __name__ == "__main__":
    main()
