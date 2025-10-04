"""Configuration management for language fixer."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class LanguagePair:
    """Configuration for a language pair."""
    name: str
    mapping_file: str
    hotkey: str
    enabled: bool = True
    mapping: Optional[Dict[str, str]] = None
    reverse_mapping: Optional[Dict[str, str]] = None


@dataclass
class Config:
    """Main configuration."""
    buffer_timeout: float = 10.0
    language_pairs: List[LanguagePair] = None

    def __post_init__(self):
        if self.language_pairs is None:
            self.language_pairs = []


def load_mapping(mapping_file: str, project_root: Path) -> tuple[Dict[str, str], Dict[str, str]]:
    """Load a mapping file and create reverse mapping.

    Args:
        mapping_file: Path to mapping JSON file (relative to project root or absolute)
        project_root: Project root directory

    Returns:
        Tuple of (forward_mapping, reverse_mapping)
    """
    # Handle absolute paths and ~ expansion
    if mapping_file.startswith('~') or mapping_file.startswith('/'):
        mapping_path = Path(mapping_file).expanduser()
    else:
        mapping_path = project_root / mapping_file

    if not mapping_path.exists():
        raise FileNotFoundError(f"Mapping file not found: {mapping_path}")

    with open(mapping_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    forward_mapping = data.get('mapping', {})

    # Create reverse mapping
    reverse_mapping = {}
    for eng_char, other_char in forward_mapping.items():
        # Handle duplicates by keeping the first occurrence
        if other_char not in reverse_mapping:
            reverse_mapping[other_char] = eng_char

    return forward_mapping, reverse_mapping


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from YAML file.

    Args:
        config_path: Path to config file. If None, looks for config.yaml in project root

    Returns:
        Config object with loaded settings
    """
    # Determine project root
    if config_path:
        config_file = Path(config_path)
        project_root = config_file.parent
    else:
        # Look for config.yaml in current directory, then parent directories
        current = Path.cwd()
        config_file = None

        for directory in [current] + list(current.parents):
            candidate = directory / "config.yaml"
            if candidate.exists():
                config_file = candidate
                project_root = directory
                break

        if not config_file:
            # No config file found, return default config
            return get_default_config()

    # Load YAML config
    if not HAS_YAML:
        raise ImportError("PyYAML is required for config files. Install with: pip install pyyaml")

    with open(config_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    # Parse config
    buffer_timeout = data.get('buffer_timeout', 10.0)

    language_pairs = []
    for pair_data in data.get('language_pairs', []):
        if not pair_data.get('enabled', True):
            continue

        mapping_file = pair_data['mapping_file']
        forward, reverse = load_mapping(mapping_file, project_root)

        pair = LanguagePair(
            name=pair_data['name'],
            mapping_file=mapping_file,
            hotkey=pair_data['hotkey'],
            enabled=pair_data.get('enabled', True),
            mapping=forward,
            reverse_mapping=reverse
        )
        language_pairs.append(pair)

    return Config(
        buffer_timeout=buffer_timeout,
        language_pairs=language_pairs
    )


def get_default_config() -> Config:
    """Get default configuration (Hebrew-English only).

    Returns:
        Config object with default settings
    """
    # Get project root (where this package is installed)
    package_root = Path(__file__).parent.parent.parent

    # Default Hebrew-English mapping
    mapping_file = "mappings/hebrew-english.json"

    try:
        forward, reverse = load_mapping(mapping_file, package_root)

        pair = LanguagePair(
            name="Hebrew-English",
            mapping_file=mapping_file,
            hotkey="cmd+shift+h",
            enabled=True,
            mapping=forward,
            reverse_mapping=reverse
        )

        return Config(
            buffer_timeout=10.0,
            language_pairs=[pair]
        )
    except FileNotFoundError:
        # Fallback to empty config if mapping file not found
        return Config(buffer_timeout=10.0, language_pairs=[])
