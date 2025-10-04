"""Language Fixer - Retroactively fix typing in wrong language."""

__version__ = "0.5.4"

from .converter import LanguageConverter
from .listener import LanguageFixer, HotkeyHandler
from .config import Config, LanguagePair, load_config, get_default_config

__all__ = [
    "LanguageFixer",
    "LanguageConverter",
    "HotkeyHandler",
    "Config",
    "LanguagePair",
    "load_config",
    "get_default_config",
]
