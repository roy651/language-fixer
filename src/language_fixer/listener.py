"""Keyboard listener and text conversion handler."""

import time
import threading
from typing import Optional, Tuple
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, Controller, Listener

from .converter import LanguageConverter
from .config import Config, LanguagePair


class HotkeyHandler:
    """Handles a single language pair and its hotkey."""

    def __init__(self, pair: LanguagePair):
        """Initialize handler for a language pair.

        Args:
            pair: LanguagePair configuration
        """
        self.pair = pair
        self.converter = LanguageConverter(pair.mapping, pair.reverse_mapping)

        # Parse hotkey (e.g., "cmd+alt+h")
        parts = pair.hotkey.lower().split('+')
        self.modifiers = set()
        self.trigger_key = None

        for part in parts:
            if part in ['cmd', 'command']:
                self.modifiers.add('cmd')
            elif part == 'shift':
                self.modifiers.add('shift')
            elif part == 'ctrl':
                self.modifiers.add('ctrl')
            elif part == 'alt':
                self.modifiers.add('alt')
            else:
                self.trigger_key = part

    def matches(self, pressed_modifiers: set, key) -> bool:
        """Check if current key press matches this hotkey.

        Args:
            pressed_modifiers: Set of currently pressed modifier keys
            key: The pressed key

        Returns:
            True if hotkey matches
        """
        if self.modifiers != pressed_modifiers:
            return False

        # Check trigger key
        if hasattr(key, 'char') and key.char and key.char.lower() == self.trigger_key:
            return True

        # Also check by virtual key code for some keys
        if self.trigger_key == 'h' and hasattr(key, 'vk') and key.vk == 4:
            return True
        if self.trigger_key == 'a' and hasattr(key, 'vk') and key.vk == 0:
            return True
        if self.trigger_key == 'r' and hasattr(key, 'vk') and key.vk == 15:
            return True

        return False


class LanguageFixer:
    """Main class for listening to keyboard and converting text."""

    def __init__(self, config: Optional[Config] = None, buffer_timeout: float = 10.0):
        """Initialize the language fixer.

        Args:
            config: Configuration object with language pairs and settings (optional)
            buffer_timeout: How long (in seconds) to keep typed text in buffer (legacy)
        """
        # Support legacy initialization
        if config is None:
            self.config = None
            self.buffer_timeout = buffer_timeout
            self.handlers = []
        else:
            self.config = config
            self.buffer_timeout = config.buffer_timeout
            self.handlers = [HotkeyHandler(pair) for pair in config.language_pairs]

        self.buffer = []
        self.last_key_time = time.time()
        self.controller = Controller()
        self.lock = threading.Lock()
        self.converting = False

        # Track modifier keys (legacy and new)
        self.cmd_pressed = False
        self.shift_pressed = False
        self.pressed_modifiers = set()

        # Last conversion tracking (for toggle-back feature)
        self.last_conversion: Optional[Tuple[str, str, Optional[HotkeyHandler]]] = None

    def should_clear_buffer(self) -> bool:
        """Check if buffer should be cleared due to timeout."""
        return time.time() - self.last_key_time > self.buffer_timeout

    def add_to_buffer(self, char: str) -> None:
        """Add character to buffer."""
        with self.lock:
            if self.should_clear_buffer():
                self.buffer.clear()
            self.buffer.append(char)
            self.last_key_time = time.time()

    def clear_buffer(self) -> None:
        """Clear the buffer."""
        with self.lock:
            self.buffer.clear()
            self.last_key_time = time.time()

    def perform_conversion(self, handler: Optional[HotkeyHandler] = None) -> None:
        """Backspace and retype with converted text.

        Args:
            handler: The hotkey handler that triggered this conversion (None for legacy mode)
        """
        with self.lock:
            if not self.buffer:
                # If buffer is empty, check if we can toggle back the last conversion
                if self.last_conversion:
                    original, converted, last_handler = self.last_conversion
                    if last_handler == handler:
                        # Toggle back - restore original text
                        self._replace_text("", original)
                        self.last_conversion = None
                return

            self.converting = True
            text = ''.join(self.buffer)

            # Convert text using handler's converter
            if handler:
                current_lang = handler.converter.detect_language(text)
                to_other = (current_lang == 'english')
                converted = handler.converter.convert_text(text, to_other)

                # Perform the replacement
                self._replace_text(text, converted)

                # Store for potential toggle-back
                self.last_conversion = (text, converted, handler)

            self.buffer.clear()
            self.converting = False

    def _switch_keyboard_layout(self) -> None:
        """Switch to the next keyboard layout using macOS shortcut.

        Uses Ctrl+Space to cycle through input sources (default macOS shortcut).
        """
        try:
            # Press Ctrl+Space to switch keyboard layout
            self.controller.press(Key.ctrl)
            time.sleep(0.05)
            self.controller.press(Key.space)
            time.sleep(0.1)
            self.controller.release(Key.space)
            time.sleep(0.05)
            self.controller.release(Key.ctrl)
            time.sleep(0.1)
        except Exception:
            # If switching fails, just continue without it
            pass

    def _replace_text(self, old_text: str, new_text: str) -> None:
        """Replace old text with new text using clipboard.

        Args:
            old_text: Text to delete (if empty, don't delete)
            new_text: Text to paste
        """
        # Save current clipboard
        try:
            old_clipboard = pyperclip.paste()
        except:
            old_clipboard = ""

        # Explicitly release all modifier keys to prevent interference
        # This prevents Cmd+Backspace behavior in browsers
        self.controller.release(Key.cmd)
        self.controller.release(Key.cmd_r)
        self.controller.release(Key.shift)
        self.controller.release(Key.shift_r)
        self.controller.release(Key.ctrl)
        self.controller.release(Key.ctrl_r)
        self.controller.release(Key.alt)
        self.controller.release(Key.alt_r)

        # Give a small delay to ensure hotkey is fully released
        time.sleep(0.15)

        # Delete original text if any
        if old_text:
            for _ in range(len(old_text)):
                self.controller.press(Key.backspace)
                self.controller.release(Key.backspace)
                time.sleep(0.01)

        # Copy converted text to clipboard
        pyperclip.copy(new_text)
        time.sleep(0.05)

        # Paste it (this handles RTL correctly)
        self.controller.press(Key.cmd)
        self.controller.press('v')
        self.controller.release('v')
        self.controller.release(Key.cmd)

        # Wait longer before switching layout to ensure paste completes
        time.sleep(0.2)

        # Switch keyboard layout to target language
        self._switch_keyboard_layout()

        # Restore old clipboard
        try:
            pyperclip.copy(old_clipboard)
        except:
            pass

    def on_press(self, key) -> None:
        """Handle key press events."""
        # Skip if we're in the middle of converting
        if self.converting:
            return

        try:
            # Track modifier keys (legacy)
            if key == Key.cmd or key == Key.cmd_r:
                self.cmd_pressed = True
                self.pressed_modifiers.add('cmd')
            elif key == Key.shift or key == Key.shift_r:
                self.shift_pressed = True
                self.pressed_modifiers.add('shift')
            elif key == Key.ctrl or key == Key.ctrl_r:
                self.pressed_modifiers.add('ctrl')
            elif key == Key.alt or key == Key.alt_r:
                self.pressed_modifiers.add('alt')
            else:
                # Check if any hotkey matches (new system)
                matched = False
                if self.handlers:
                    for handler in self.handlers:
                        if handler.matches(self.pressed_modifiers, key):
                            threading.Thread(target=self.perform_conversion, args=(handler,)).start()
                            matched = True
                            break

                # Legacy hotkey check (for backward compatibility)
                if not matched and not self.handlers:
                    if hasattr(key, 'vk') and key.vk == 4 and self.cmd_pressed and self.shift_pressed:
                        threading.Thread(target=self.perform_conversion).start()
                        matched = True
                    elif hasattr(key, 'char') and key.char in ['h', 'H', 'י'] and self.cmd_pressed and self.shift_pressed:
                        threading.Thread(target=self.perform_conversion).start()
                        matched = True

                if matched:
                    # Event matched - don't process as regular character
                    return

                # Handle backspace - remove last character from buffer
                if key == Key.backspace:
                    with self.lock:
                        if self.buffer:
                            self.buffer.pop()
                            self.last_key_time = time.time()
                # Handle space key specially
                elif key == Key.space:
                    self.add_to_buffer(' ')
                # Regular character - add to buffer
                elif hasattr(key, 'char') and key.char:
                    self.add_to_buffer(key.char)
                # Clear buffer on special keys
                elif key in [Key.enter, Key.tab, Key.up, Key.down, Key.left, Key.right,
                            Key.home, Key.end, Key.page_up, Key.page_down]:
                    self.clear_buffer()
                    # Clear last conversion on navigation
                    self.last_conversion = None

        except AttributeError:
            pass

    def on_release(self, key):
        """Handle key release events."""
        if key == Key.cmd or key == Key.cmd_r:
            self.cmd_pressed = False
            self.pressed_modifiers.discard('cmd')
        elif key == Key.shift or key == Key.shift_r:
            self.shift_pressed = False
            self.pressed_modifiers.discard('shift')
        elif key == Key.ctrl or key == Key.ctrl_r:
            self.pressed_modifiers.discard('ctrl')
        elif key == Key.alt or key == Key.alt_r:
            self.pressed_modifiers.discard('alt')

        # Exit on Cmd+Esc
        if key == Key.esc and (self.cmd_pressed or 'cmd' in self.pressed_modifiers):
            return False

    def start(self) -> None:
        """Start listening to keyboard events."""
        print("Language Fixer started!")
        print(f"Buffer timeout: {self.buffer_timeout} seconds")

        if self.handlers:
            print("\nActive language pairs:")
            for handler in self.handlers:
                print(f"  - {handler.pair.name}: {handler.pair.hotkey}")
        else:
            print("Hotkey: Cmd+Option+H (or Cmd+Option+י in Hebrew) to convert text")

        print("\nPress Cmd+Esc to quit")
        if self.handlers:
            print("\nFeatures:")
            print("  - Press hotkey to convert text between languages")
            print("  - Press hotkey again (on empty buffer) to toggle back\n")

        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
