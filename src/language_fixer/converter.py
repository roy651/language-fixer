"""Text conversion logic for keyboard layouts."""

from typing import Dict, Tuple

# Legacy mappings for backward compatibility (used in tests)
ENG_TO_HEB = {
    'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף',
    'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ', '/': '.',
    # Uppercase
    'Q': '/', 'W': "'", 'E': 'ק', 'R': 'ר', 'T': 'א', 'Y': 'ט', 'U': 'ו', 'I': 'ן', 'O': 'ם', 'P': 'פ',
    'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י', 'J': 'ח', 'K': 'ל', 'L': 'ך', ':': 'ף',
    'Z': 'ז', 'X': 'ס', 'C': 'ב', 'V': 'ה', 'B': 'נ', 'N': 'מ', 'M': 'צ', '<': 'ת', '>': 'ץ', '?': '.',
}

HEB_TO_ENG = {v: k for k, v in ENG_TO_HEB.items() if v not in ['/', "'", 'ק', 'ר', 'א', 'ט', 'ו', 'ן', 'ם', 'פ', 'ש', 'ד', 'ג', 'כ', 'ע', 'י', 'ח', 'ל', 'ך', 'ף', 'ז', 'ס', 'ב', 'ה', 'נ', 'מ', 'צ', 'ת', 'ץ', '.']}
# Properly create reverse for unique values
for k, v in ENG_TO_HEB.items():
    if v not in HEB_TO_ENG:
        HEB_TO_ENG[v] = k


class LanguageConverter:
    """Handles text conversion between two keyboard layouts."""

    def __init__(self, forward_mapping: Dict[str, str], reverse_mapping: Dict[str, str]):
        """Initialize converter with mappings.

        Args:
            forward_mapping: English -> Other language mapping
            reverse_mapping: Other language -> English mapping
        """
        self.forward_mapping = forward_mapping
        self.reverse_mapping = reverse_mapping

    def convert_text(self, text: str, to_other: bool = True) -> str:
        """Convert text from one language to another.

        Args:
            text: The text to convert
            to_other: If True, convert English to other; otherwise other to English

        Returns:
            The converted text
        """
        mapping = self.forward_mapping if to_other else self.reverse_mapping
        result = []
        for char in text:
            result.append(mapping.get(char, char))
        return ''.join(result)

    def detect_language(self, text: str) -> str:
        """Detect if text is primarily in other language or English.

        Args:
            text: The text to analyze

        Returns:
            'other' if text contains more other-language characters, 'english' otherwise
        """
        other_count = sum(1 for c in text if c in self.reverse_mapping)
        english_count = sum(1 for c in text if c in self.forward_mapping and c.isalpha())
        return 'other' if other_count > english_count else 'english'


# Legacy functions for backward compatibility (used in tests)
def convert_text(text: str, to_hebrew: bool = True) -> str:
    """Convert text from one language to another.

    Args:
        text: The text to convert
        to_hebrew: If True, convert English to Hebrew; otherwise Hebrew to English

    Returns:
        The converted text
    """
    mapping = ENG_TO_HEB if to_hebrew else HEB_TO_ENG
    result = []
    for char in text:
        result.append(mapping.get(char, char))
    return ''.join(result)


def detect_language(text: str) -> str:
    """Detect if text is primarily Hebrew or English.

    Args:
        text: The text to analyze

    Returns:
        'hebrew' if text contains more Hebrew characters, 'english' otherwise
    """
    hebrew_count = sum(1 for c in text if c in HEB_TO_ENG)
    english_count = sum(1 for c in text if c in ENG_TO_HEB and c.isalpha())
    return 'hebrew' if hebrew_count > english_count else 'english'
