"""Text conversion logic for keyboard layouts."""

from typing import Dict


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
