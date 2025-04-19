"""
Handles global keyboard listeners, including hotkeys.
Contains the CustomListener class and neighbor-key definitions
for realistic typos, if needed.
"""

import random
import string
from pynput.keyboard import Listener, Key, KeyCode
from . import typing_engine

# Keyboard layout mapping for realistic typos
KEYBOARD_NEIGHBORS = {
    'q': ['w','a','s'],
    'w': ['q','e','a','s','d'],
    'e': ['w','r','s','d','f'],
    'r': ['e','t','d','f','g'],
    't': ['r','y','f','g','h'],
    'y': ['t','u','g','h','j'],
    'u': ['y','i','h','j','k'],
    'i': ['u','o','j','k','l'],
    'o': ['i','p','k','l'],
    'p': ['o','l'],
    'a': ['q','w','s','z'],
    's': ['w','e','d','x','z','a'],
    'd': ['e','r','f','c','x','s'],
    'f': ['r','t','g','v','c','d'],
    'g': ['t','y','h','b','v','f'],
    'h': ['y','u','j','n','b','g'],
    'j': ['u','i','k','m','n','h'],
    'k': ['i','o','l','m','j'],
    'l': ['o','p','k'],
    'z': ['a','s','x'],
    'x': ['s','d','c','z'],
    'c': ['d','f','v','x'],
    'v': ['f','g','b','c'],
    'b': ['g','h','n','v'],
    'n': ['h','j','m','b'],
    'm': ['j','k','n']
}

class CustomListener(Listener):
    """
    Custom listener to track modifier keys and numeric keys.
    """
    def __init__(self, on_press, *args, **kwargs):
        super().__init__(on_press, *args, **kwargs)
        self.ctrl_pressed = False  # or self.cmd_pressed on Mac
        self.num_pressed = None

    def on_press(self, key):
        if key == Key.cmd or key == Key.ctrl_l or key == Key.ctrl_r:
            self.ctrl_pressed = True
        elif key in [KeyCode(char='1'), KeyCode(char='2'), KeyCode(char='3')]:
            self.num_pressed = int(key.char)
        return super().on_press(key)

    def on_release(self, key):
        if key == Key.cmd or key == Key.ctrl_l or key == Key.ctrl_r:
            self.ctrl_pressed = False
        elif key in [KeyCode(char='1'), KeyCode(char='2'), KeyCode(char='3')]:
            self.num_pressed = None
        return super().on_release(key)

def on_press(key):
    """
    Global on_press callback for the CustomListener.
    F9 = start typing
    ESC = stop typing
    """
    # Start typing on F9
    if key == Key.f9:
        typing_engine.start_typing_thread()
    
    # Stop typing on Escape
    elif key == Key.esc:
        typing_engine.stop_typing = True

def start_listener():
    """
    Initialize and start the CustomListener in blocking mode.
    This function is designed to be called in a separate thread.
    """
    with CustomListener(on_press=on_press) as listener:
        listener.run()
