"""Tests for text conversion logic."""

import json
from pathlib import Path
import pytest
from language_fixer.converter import LanguageConverter


# Load Hebrew mappings for tests
def _load_hebrew_converter():
    mappings_file = Path(__file__).parent.parent / "mappings" / "hebrew-english.json"
    with open(mappings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    forward = data['mapping']
    reverse = {}
    for k, v in sorted(forward.items(), key=lambda x: (x[0].isupper(), x[0])):
        if v not in reverse:
            reverse[v] = k
    return LanguageConverter(forward, reverse)


converter = _load_hebrew_converter()
ENG_TO_HEB = converter.forward_mapping
HEB_TO_ENG = converter.reverse_mapping


class TestConvertText:
    """Test text conversion between English and Hebrew."""

    def test_english_to_hebrew_simple(self):
        """Test simple English to Hebrew conversion."""
        # "hello" typed in English converts to Hebrew keys at same positions
        assert converter.convert_text("hello", to_other=True) == "יקךךם"

    def test_hebrew_to_english_simple(self):
        """Test simple Hebrew to English conversion."""
        # "שלום" typed in Hebrew converts to English keys at same positions
        assert converter.convert_text("שלום", to_other=False) == "akuo"

    def test_english_to_hebrew_with_spaces(self):
        """Test conversion with spaces preserved."""
        assert converter.convert_text("hello world", to_other=True) == "יקךךם ׳םרךג"

    def test_mixed_characters_preserved(self):
        """Test that unmapped characters are preserved."""
        result = converter.convert_text("hello123", to_other=True)
        assert "123" in result

    def test_empty_string(self):
        """Test conversion of empty string."""
        assert converter.convert_text("", to_other=True) == ""
        assert converter.convert_text("", to_other=False) == ""

    def test_punctuation_conversion(self):
        """Test that punctuation is converted correctly."""
        assert converter.convert_text("q", to_other=True) == "/"
        assert converter.convert_text("/", to_other=True) == "."

    def test_hebrew_geresh_conversion(self):
        """Test that Hebrew geresh (׳) is converted correctly."""
        # 'w' should convert to Hebrew geresh ׳ (not ASCII apostrophe ')
        assert converter.convert_text("w", to_other=True) == "׳"
        # Hebrew geresh should convert back to 'w'
        assert converter.convert_text("׳", to_other=False) == "w"
        # Test the word "how" typed in Hebrew: ים׳
        assert converter.convert_text("ים׳", to_other=False) == "how"


class TestDetectLanguage:
    """Test language detection."""

    def test_detect_hebrew(self):
        """Test detection of Hebrew text."""
        assert converter.detect_language("שלום") == "other"

    def test_detect_english(self):
        """Test detection of English text."""
        assert converter.detect_language("hello") == "english"

    def test_detect_mixed_hebrew_dominant(self):
        """Test detection when Hebrew characters dominate."""
        assert converter.detect_language("שלום123abc") == "other"

    def test_detect_mixed_english_dominant(self):
        """Test detection when English characters dominate."""
        assert converter.detect_language("hello123ש") == "english"

    def test_detect_empty_string(self):
        """Test detection of empty string defaults to English."""
        assert converter.detect_language("") == "english"


class TestMappings:
    """Test keyboard mapping dictionaries."""

    def test_eng_to_heb_has_common_keys(self):
        """Test that common keys are mapped."""
        assert 'a' in ENG_TO_HEB
        assert 's' in ENG_TO_HEB
        assert 'd' in ENG_TO_HEB

    def test_heb_to_eng_is_reverse(self):
        """Test that Hebrew to English mapping is properly reversed (for unique mappings)."""
        # Note: Some chars like 'i'/'b' both map to 'ן', so not all are reversible
        # Test a subset that should work
        test_chars = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'n', 'm']
        for eng_char in test_chars:
            heb_char = ENG_TO_HEB[eng_char]
            assert HEB_TO_ENG.get(heb_char) == eng_char

    def test_mappings_symmetry(self):
        """Test that mappings are symmetric (except for duplicates)."""
        # Convert English to Hebrew and back
        eng_chars = "hello"
        heb_text = converter.convert_text(eng_chars, to_other=True)
        back_to_eng = converter.convert_text(heb_text, to_other=False)
        assert back_to_eng == eng_chars
