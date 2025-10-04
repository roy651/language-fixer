"""Tests for text conversion logic."""

import pytest
from language_fixer.converter import convert_text, detect_language, ENG_TO_HEB, HEB_TO_ENG


class TestConvertText:
    """Test text conversion between English and Hebrew."""

    def test_english_to_hebrew_simple(self):
        """Test simple English to Hebrew conversion."""
        # "hello" typed in English converts to Hebrew keys at same positions
        assert convert_text("hello", to_hebrew=True) == "יקךךם"

    def test_hebrew_to_english_simple(self):
        """Test simple Hebrew to English conversion."""
        # "שלום" typed in Hebrew converts to English keys at same positions
        assert convert_text("שלום", to_hebrew=False) == "akuo"

    def test_english_to_hebrew_with_spaces(self):
        """Test conversion with spaces preserved."""
        assert convert_text("hello world", to_hebrew=True) == "יקךךם 'םרךג"

    def test_mixed_characters_preserved(self):
        """Test that unmapped characters are preserved."""
        result = convert_text("hello123", to_hebrew=True)
        assert "123" in result

    def test_empty_string(self):
        """Test conversion of empty string."""
        assert convert_text("", to_hebrew=True) == ""
        assert convert_text("", to_hebrew=False) == ""

    def test_punctuation_conversion(self):
        """Test that punctuation is converted correctly."""
        assert convert_text("q", to_hebrew=True) == "/"
        assert convert_text("/", to_hebrew=True) == "."


class TestDetectLanguage:
    """Test language detection."""

    def test_detect_hebrew(self):
        """Test detection of Hebrew text."""
        assert detect_language("שלום") == "hebrew"

    def test_detect_english(self):
        """Test detection of English text."""
        assert detect_language("hello") == "english"

    def test_detect_mixed_hebrew_dominant(self):
        """Test detection when Hebrew characters dominate."""
        assert detect_language("שלום123abc") == "hebrew"

    def test_detect_mixed_english_dominant(self):
        """Test detection when English characters dominate."""
        assert detect_language("hello123ש") == "english"

    def test_detect_empty_string(self):
        """Test detection of empty string defaults to English."""
        assert detect_language("") == "english"


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
        heb_text = convert_text(eng_chars, to_hebrew=True)
        back_to_eng = convert_text(heb_text, to_hebrew=False)
        assert back_to_eng == eng_chars
