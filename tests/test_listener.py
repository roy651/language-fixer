"""Tests for keyboard listener and buffer management."""

import time
from unittest.mock import Mock
from pynput.keyboard import Key, KeyCode
import pytest

from language_fixer.listener import LanguageFixer
from language_fixer.config import Config, LanguagePair


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Mock(spec=Config)
    config.buffer_timeout = 10.0

    # Mock language pair
    lang_pair = Mock(spec=LanguagePair)
    lang_pair.name = "Test-Language"
    lang_pair.hotkey = "cmd+shift+t"
    lang_pair.enabled = True

    # Mock converter
    mock_converter = Mock()
    mock_converter.convert_text.return_value = "converted"
    lang_pair.converter = mock_converter

    config.language_pairs = [lang_pair]
    return config


class TestBufferManagement:
    """Test buffer management and backspace handling."""

    def test_buffer_stores_characters(self, mock_config):
        """Test that regular characters are added to buffer."""
        fixer = LanguageFixer(mock_config)

        # Simulate typing 'h', 'e', 'l', 'l', 'o'
        for char in "hello":
            key = KeyCode.from_char(char)
            fixer.on_press(key)

        with fixer.lock:
            assert fixer.buffer == list("hello")

    def test_backspace_removes_from_buffer(self, mock_config):
        """Test that backspace removes the last character from buffer."""
        fixer = LanguageFixer(mock_config)

        # Type "hello"
        for char in "hello":
            key = KeyCode.from_char(char)
            fixer.on_press(key)

        # Press backspace twice
        fixer.on_press(Key.backspace)
        fixer.on_press(Key.backspace)

        with fixer.lock:
            assert fixer.buffer == list("hel")

    def test_backspace_on_empty_buffer(self, mock_config):
        """Test that backspace on empty buffer doesn't cause errors."""
        fixer = LanguageFixer(mock_config)

        # Press backspace on empty buffer
        fixer.on_press(Key.backspace)

        with fixer.lock:
            assert fixer.buffer == []

    def test_space_added_to_buffer(self, mock_config):
        """Test that space is added to the buffer."""
        fixer = LanguageFixer(mock_config)

        # Type "hello"
        for char in "hello":
            key = KeyCode.from_char(char)
            fixer.on_press(key)

        # Press space
        fixer.on_press(Key.space)

        with fixer.lock:
            assert fixer.buffer == list("hello ")

    def test_buffer_timeout_updates(self, mock_config):
        """Test that buffer timeout is updated on key press."""
        fixer = LanguageFixer(mock_config)

        initial_time = fixer.last_key_time
        time.sleep(0.01)  # Small delay

        # Type a character
        fixer.on_press(KeyCode.from_char('a'))

        assert fixer.last_key_time > initial_time

    def test_backspace_updates_timeout(self, mock_config):
        """Test that backspace also updates the timeout."""
        fixer = LanguageFixer(mock_config)

        # Type a character
        fixer.on_press(KeyCode.from_char('a'))
        initial_time = fixer.last_key_time

        time.sleep(0.01)  # Small delay

        # Press backspace
        fixer.on_press(Key.backspace)

        assert fixer.last_key_time > initial_time


class TestConversionWithBackspace:
    """Test that conversion works correctly with backspace."""

    def test_conversion_excludes_deleted_chars(self, mock_config):
        """Test that backspace-deleted characters are not converted."""
        fixer = LanguageFixer(mock_config)

        # Type "hello"
        for char in "hello":
            key = KeyCode.from_char(char)
            fixer.on_press(key)

        # Delete last two characters with backspace
        fixer.on_press(Key.backspace)
        fixer.on_press(Key.backspace)

        # Trigger conversion (this would be done by hotkey handler)
        with fixer.lock:
            buffer_text = ''.join(fixer.buffer)

        # Verify only "hel" remains in buffer (not "hello")
        assert buffer_text == "hel"
        assert len(fixer.buffer) == 3
