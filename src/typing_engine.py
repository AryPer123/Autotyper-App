"""
Handles the core typing logic, including WPM calculations,
random pauses, typos, and the actual keystroke simulation.
"""

import time
import random
import string
import threading
from pynput.keyboard import Controller, Key
from .keyboard_utils import KEYBOARD_NEIGHBORS

keyboard = Controller()
stop_typing = False  # Global flag to halt typing

def wpm_to_cps(wpm):
    """Convert Words Per Minute to Characters Per Second."""
    # Average word length is considered 5 characters
    return (wpm * 5) / 60

def cps_to_wpm(cps):
    """Convert Characters Per Second to Words Per Minute."""
    return (cps * 60) / 5

def get_typo_length():
    """Generate typo length with weighted probability."""
    # Example probability distribution for lengths 1 to 5
    weights = [0.5, 0.25, 0.15, 0.07, 0.03]  # Probabilities
    return random.choices([1, 2, 3, 4, 5], weights=weights)[0]

def make_typo(char, typo_length):
    """Create a realistic typo based on keyboard proximity."""
    if char.lower() not in KEYBOARD_NEIGHBORS:
        # If char isn't in the neighbor map, return random letters
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(typo_length))
    
    typo_chars = []
    for _ in range(typo_length):
        if random.random() < 0.7:  # 70% chance of using a neighbor key
            base_char = char.lower()
            typo_char = random.choice(KEYBOARD_NEIGHBORS[base_char])
        else:
            typo_char = random.choice(string.ascii_lowercase)
        typo_chars.append(typo_char)
    return ''.join(typo_chars)

def type_text(text, 
              min_wpm=40.0, 
              max_wpm=80.0, 
              delay=0.25,
              thinking_enabled=True,
              min_pause=0.5,
              max_pause=2.0,
              pause_frequency=50,
              typos_enabled=True,
              typo_chance=0.3,
              random_letters=False):
    """
    Core function to type out the given text with human-like patterns.
    This runs synchronously; consider starting it in a separate thread.
    """
    global stop_typing
    stop_typing = False

    # Convert WPM to characters per second
    min_cps = wpm_to_cps(min_wpm)
    max_cps = wpm_to_cps(max_wpm)

    # Initial delay before typing starts
    time.sleep(delay)

    # Optionally inject random letters into the text
    if random_letters:
        modified_text = []
        i = 0
        while i < len(text):
            modified_text.append(text[i])
            # Randomly inject a letter
            if random.randint(8, 15) == len(modified_text) % random.randint(8, 15):
                modified_text.append(random.choice(string.ascii_letters))
            i += 1
        text = ''.join(modified_text)

    chars_typed = 0
    current_speed = random.uniform(min_cps, max_cps)
    speed_change_counter = 0

    # Split text into paragraphs by newline
    lines = text.split('\n')

    for line_num, line in enumerate(lines):
        if stop_typing:
            break

        words = line.split()
        for word_num, word in enumerate(words):
            if stop_typing:
                break

            # Randomly change typing speed every few words
            speed_change_counter += 1
            if speed_change_counter >= random.randint(3, 8):
                current_speed = random.uniform(min_cps, max_cps)
                speed_change_counter = 0

            current_delay = 1 / current_speed

            # Decide if a typo will be made in this word
            make_typo_here = (
                typos_enabled and 
                len(word) >= 3 and 
                random.random() < typo_chance
            )
            typo_pos = random.randint(0, len(word)-1) if make_typo_here else -1

            for i, char in enumerate(word):
                if stop_typing:
                    break

                # Thinking pause logic
                if thinking_enabled:
                    chars_typed += 1
                    if chars_typed % pause_frequency == 0:
                        thinking_time = random.uniform(min_pause, max_pause)
                        time.sleep(thinking_time)
                        # Randomize speed again after pause
                        current_speed = random.uniform(min_cps, max_cps)
                        current_delay = 1 / current_speed

                # Press the actual character
                keyboard.press(char)
                keyboard.release(char)
                time.sleep(current_delay)

                # Insert a typo at the designated position
                if i == typo_pos and not stop_typing:
                    time.sleep(random.uniform(0.1, 0.2))
                    t_length = get_typo_length()
                    typo_str = make_typo(char, t_length)

                    # Type the typo
                    for t_char in typo_str:
                        keyboard.press(t_char)
                        keyboard.release(t_char)
                        time.sleep(current_delay)

                    # Small pause before correction
                    time.sleep(random.uniform(0.2, 0.4))

                    # Delete the typo
                    for _ in range(len(typo_str)):
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                        time.sleep(current_delay * 0.5)

                    time.sleep(random.uniform(0.1, 0.2))

            # Press space after each word (unless it's the last word in the line)
            if word_num < len(words) - 1 and not stop_typing:
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                time.sleep(current_delay)

        # Press Enter twice after each line (paragraph separation)
        if line_num < len(lines) - 1 and not stop_typing:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(current_delay)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(current_delay * 2)

def start_typing_thread():
    """
    Helper function to start typing_text in a separate thread.
    Pulls the current config from the GUI, if available.
    """
    from .gui import get_current_typing_config
    config = get_current_typing_config()
    # Start type_text in a new thread
    t = threading.Thread(
        target=type_text, 
        kwargs=config,
        daemon=True
    )
    t.start()
