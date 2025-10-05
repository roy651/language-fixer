#!/usr/bin/env python3
"""Interactive mapping generator for custom language pairs."""

import json
import sys
from pathlib import Path


QWERTY_KEYS = [
    # Row 1
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
    # Row 2
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",
    # Row 3
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
]

QWERTY_KEYS_UPPERCASE = [
    # Row 1
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}',
    # Row 2
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"',
    # Row 3
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?',
]


def print_keyboard_layout():
    """Display visual keyboard layout."""
    print("\nQWERTY Keyboard Layout:")
    print("┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐")
    print("│  Q  │  W  │  E  │  R  │  T  │  Y  │  U  │  I  │  O  │  P  │  [  │  ]  │")
    print("├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
    print("│  A  │  S  │  D  │  F  │  G  │  H  │  J  │  K  │  L  │  ;  │  '  │     │")
    print("├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤")
    print("│  Z  │  X  │  C  │  V  │  B  │  N  │  M  │  ,  │  .  │  /  │     │     │")
    print("└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
    print()


def generate_mapping_interactive():
    """Generate a mapping file interactively."""
    print("=" * 60)
    print("Language Fixer - Mapping Generator")
    print("=" * 60)
    print("\nThis tool helps you create a custom keyboard layout mapping.")
    print("You'll type the character from your other language for each key.")
    print()

    # Get metadata
    lang_name = input("Enter language pair name (e.g., 'French-English'): ").strip()
    description = input("Enter description (optional): ").strip() or f"{lang_name} keyboard mapping"

    print("\n" + "=" * 60)
    print("Switch to your other keyboard layout now!")
    print("=" * 60)
    print("\nFor each key shown, type the character that appears when you")
    print("press that key in your OTHER language layout.")
    print("Press ENTER to skip a key if it's the same as English.\n")

    input("Press ENTER when ready to start...")
    print()

    mapping = {}

    # Lowercase keys
    print("\n--- Lowercase Keys ---")
    print_keyboard_layout()

    for key in QWERTY_KEYS:
        while True:
            char = input(f"Press '{key}' in your layout (or ENTER to skip): ").strip()
            if char == "":
                # Skip - same as English
                break
            if len(char) == 1:
                mapping[key] = char
                break
            print("Please enter exactly one character.")

    # Uppercase keys (with Shift)
    print("\n--- Uppercase Keys (with Shift) ---")
    print("Now press Shift + each key in your layout")
    print()

    for key in QWERTY_KEYS_UPPERCASE:
        while True:
            char = input(f"Press Shift+'{key}' in your layout (or ENTER to skip): ").strip()
            if char == "":
                # Skip - same as English
                break
            if len(char) >= 1:  # Allow multi-char for some languages
                mapping[key] = char
                break
            print("Please enter at least one character.")

    # Create output
    output = {
        "name": lang_name,
        "description": description,
        "mapping": mapping
    }

    # Save file
    filename = lang_name.lower().replace(" ", "-").replace("/", "-") + ".json"
    output_path = Path("mappings") / filename

    # Create mappings directory if it doesn't exist
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"✓ Mapping saved to: {output_path}")
    print("=" * 60)
    print(f"\nTotal keys mapped: {len(mapping)}")
    print("\nTo use this mapping:")
    print(f"1. Add it to your config.yaml:")
    print(f"   - name: \"{lang_name}\"")
    print(f"     mapping_file: \"{output_path}\"")
    print(f"     hotkey: \"cmd+alt+<key>\"")
    print(f"     enabled: true")
    print("\n2. Restart language-fixer")
    print()


def main():
    """Entry point for mapping generator."""
    try:
        generate_mapping_interactive()
    except KeyboardInterrupt:
        print("\n\nAborted.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
