"""Language Fixer - Retroactively fix typing in wrong language."""

__version__ = "0.2.5"

from .converter import convert_text, detect_language, ENG_TO_HEB, HEB_TO_ENG, LanguageConverter
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
    "convert_text",
    "detect_language",
    "ENG_TO_HEB",
    "HEB_TO_ENG",
]
