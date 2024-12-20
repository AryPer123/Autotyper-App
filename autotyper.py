import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Controller, Listener, Key, KeyCode
import time
import threading
import random
import string
import pyperclip

# Initialize keyboard controller
keyboard = Controller()

# Flag to stop typing
stop_typing = False

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

def wpm_to_cps(wpm):
    """Convert Words Per Minute to Characters Per Second"""
    # Average word length is 5 characters
    return (wpm * 5) / 60

def cps_to_wpm(cps):
    """Convert Characters Per Second to Words Per Minute"""
    return (cps * 60) / 5

def make_typo(char, typo_length):
    """Create a realistic typo based on keyboard proximity"""
    if not char.lower() in KEYBOARD_NEIGHBORS:
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

def get_typo_length():
    """Generate typo length with weighted probability"""
    weights = [0.5, 0.25, 0.15, 0.07, 0.03]  # Probabilities for lengths 1-5
    return random.choices([1, 2, 3, 4, 5], weights=weights)[0]

# Function to type out the text
def type_text():
    global stop_typing
    stop_typing = False
    text = text_input.get("1.0", tk.END).strip()
    
    # Helper functions for WPM conversion
    def wpm_to_cps(wpm):
        """Convert Words Per Minute to Characters Per Second"""
        return (wpm * 5) / 60

    def cps_to_wpm(cps):
        """Convert Characters Per Second to Words Per Minute"""
        return (cps * 60) / 5
    
    # Convert WPM to characters per second
    min_wpm = float(min_speed_entry.get())
    max_wpm = float(max_speed_entry.get())
    min_cps = wpm_to_cps(min_wpm)
    max_cps = wpm_to_cps(max_wpm)
    
    delay = float(delay_entry.get())
    
    # Get thinking pause settings
    thinking_enabled = thinking_toggle_var.get()
    min_pause = float(min_pause_entry.get())
    max_pause = float(max_pause_entry.get())
    pause_frequency = int(pause_freq_entry.get())
    
    # Get typo settings
    typos_enabled = typo_toggle_var.get()
    typo_chance = float(typo_freq_entry.get()) / 100
    
    time.sleep(delay)

    if random_toggle_var.get():
        modified_text = []
        i = 0
        while i < len(text):
            modified_text.append(text[i])
            if random.randint(8, 15) == len(modified_text) % random.randint(8, 15):
                modified_text.append(random.choice(string.ascii_letters))
            i += 1
        text = ''.join(modified_text)
    
    chars_typed = 0
    current_speed = random.uniform(min_cps, max_cps)
    speed_change_counter = 0
    
    # Split text into paragraphs
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
            if speed_change_counter >= random.randint(3, 8):  # Change speed every 3-8 words
                current_speed = random.uniform(min_cps, max_cps)
                speed_change_counter = 0

            # Calculate current delay between keystrokes
            current_delay = 1 / current_speed

            make_typo_here = typos_enabled and len(word) >= 3 and random.random() < typo_chance
            typo_pos = random.randint(0, len(word)-1) if make_typo_here else -1

            for i, char in enumerate(word):
                if stop_typing:
                    break

                if thinking_enabled:
                    chars_typed += 1
                    if chars_typed % pause_frequency == 0:
                        thinking_time = random.uniform(min_pause, max_pause)
                        time.sleep(thinking_time)
                        # Randomize speed again after pause
                        current_speed = random.uniform(min_cps, max_cps)

                keyboard.press(char)
                keyboard.release(char)
                time.sleep(current_delay)

                if i == typo_pos:
                    time.sleep(random.uniform(0.1, 0.2))
                    typo_length = get_typo_length()
                    typo = make_typo(char, typo_length)
                    
                    # Type the typo
                    for typo_char in typo:
                        keyboard.press(typo_char)
                        keyboard.release(typo_char)
                        time.sleep(current_delay)

                    # Pause before correction
                    time.sleep(random.uniform(0.2, 0.4))

                    # Delete the typo
                    for _ in range(len(typo)):
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                        time.sleep(current_delay * 0.5)

                    time.sleep(random.uniform(0.1, 0.2))

            if word_num < len(words) - 1:
                keyboard.press(Key.space)
                keyboard.release(Key.space)
                time.sleep(current_delay)
        
        if line_num < len(lines) - 1:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(current_delay)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(current_delay * 2)

# Function to listen for the global hotkey to start typing or stop typing
def on_press(key):
    global stop_typing
    try:
        if key == Key.f9:  # Set F9 as the shortcut key to start typing
            threading.Thread(target=type_text).start()
        elif key == Key.esc:  # Press Escape to stop typing
            stop_typing = True
        elif key == Key.cmd and listener.ctrl_pressed:
            if listener.num_pressed == 1:
                text_input.focus_set()
            elif listener.num_pressed == 2:
                min_speed_entry.focus_set()
            elif listener.num_pressed == 3:
                delay_entry.focus_set()
    except AttributeError:
        pass

# Custom listener class to track modifier keys and numbers
class CustomListener(Listener):
    def __init__(self, on_press, *args, **kwargs):
        super().__init__(on_press, *args, **kwargs)
        self.ctrl_pressed = False
        self.num_pressed = None

    def on_press(self, key):
        if key == Key.cmd:
            self.ctrl_pressed = True
        elif key in [KeyCode(char='1'), KeyCode(char='2'), KeyCode(char='3')]:
            self.num_pressed = int(key.char)
        return super().on_press(key)

    def on_release(self, key):
        if key == Key.cmd:
            self.ctrl_pressed = False
        elif key in [KeyCode(char='1'), KeyCode(char='2'), KeyCode(char='3')]:
            self.num_pressed = None
        return super().on_release(key)

# Function to constantly update the text box with clipboard content
def update_clipboard():
    """Update the text box with clipboard content"""
    def update_text():
        if clipboard_option_var.get():
            try:
                clipboard_text = pyperclip.paste()
                current_text = text_input.get("1.0", tk.END).strip()
                if clipboard_text != current_text:
                    text_input.delete("1.0", tk.END)
                    text_input.insert("1.0", clipboard_text)
            except Exception as e:
                print(f"Error updating clipboard: {e}")
    
    while True:
        try:
            root.after(1000, update_text)  # Schedule the update on the main thread
            time.sleep(1)
        except Exception as e:
            print(f"Error in clipboard thread: {e}")

# Set up the GUI
root = tk.Tk()
root.title("Auto Typer")

# Create main frame with scrollbar support
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Textbox for input
text_label = ttk.Label(main_frame, text="Enter text to type:")
text_label.pack(pady=5)
text_input = tk.Text(main_frame, height=10, width=50)
text_input.pack(pady=5)

# Frame for settings
settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
settings_frame.pack(fill=tk.X, pady=5)

# Left column
left_column = ttk.Frame(settings_frame)
left_column.pack(side=tk.LEFT, padx=5)

# Clipboard or manual text selection
clipboard_option_var = tk.BooleanVar(value=True)
clipboard_option = ttk.Checkbutton(left_column, text="Use clipboard text", variable=clipboard_option_var)
clipboard_option.pack(anchor=tk.W)

# Random letters toggle
random_toggle_var = tk.BooleanVar()
random_toggle = ttk.Checkbutton(left_column, text="Add random letters", variable=random_toggle_var)
random_toggle.pack(anchor=tk.W)

# Right column
right_column = ttk.Frame(settings_frame)
right_column.pack(side=tk.LEFT, padx=5)

# Typing speed entry
speed_frame = ttk.Frame(settings_frame)
speed_frame.pack(fill=tk.X, pady=2)
min_speed_label = ttk.Label(speed_frame, text="Min typing speed (WPM):")
min_speed_label.pack(side=tk.LEFT)
min_speed_entry = ttk.Entry(speed_frame, width=8)
min_speed_entry.insert(0, "40")  # Default 40 WPM
min_speed_entry.pack(side=tk.LEFT, padx=5)

max_speed_label = ttk.Label(speed_frame, text="Max typing speed (WPM):")
max_speed_label.pack(side=tk.LEFT, padx=(10, 0))
max_speed_entry = ttk.Entry(speed_frame, width=8)
max_speed_entry.insert(0, "80")  # Default 80 WPM
max_speed_entry.pack(side=tk.LEFT, padx=5)

# Initial delay entry
delay_frame = ttk.Frame(right_column)
delay_frame.pack(fill=tk.X, pady=2)
delay_label = ttk.Label(delay_frame, text="Start delay (sec):")
delay_label.pack(side=tk.LEFT)
delay_entry = ttk.Entry(delay_frame, width=8)
delay_entry.insert(0, "0.25")
delay_entry.pack(side=tk.LEFT, padx=5)

# Thinking pauses frame
thinking_frame = ttk.LabelFrame(main_frame, text="Thinking Pauses", padding=10)
thinking_frame.pack(fill=tk.X, pady=5)

# Enable thinking pauses
thinking_toggle_var = tk.BooleanVar(value=True)
thinking_toggle = ttk.Checkbutton(thinking_frame, text="Enable random thinking pauses", variable=thinking_toggle_var)
thinking_toggle.pack(anchor=tk.W)

# Thinking settings
pause_settings_frame = ttk.Frame(thinking_frame)
pause_settings_frame.pack(fill=tk.X, pady=5)

# Minimum pause
min_pause_frame = ttk.Frame(pause_settings_frame)
min_pause_frame.pack(side=tk.LEFT, padx=5)
min_pause_label = ttk.Label(min_pause_frame, text="Min pause (sec):")
min_pause_label.pack(side=tk.LEFT)
min_pause_entry = ttk.Entry(min_pause_frame, width=6)
min_pause_entry.insert(0, "0.5")
min_pause_entry.pack(side=tk.LEFT, padx=2)

# Maximum pause
max_pause_frame = ttk.Frame(pause_settings_frame)
max_pause_frame.pack(side=tk.LEFT, padx=5)
max_pause_label = ttk.Label(max_pause_frame, text="Max pause (sec):")
max_pause_label.pack(side=tk.LEFT)
max_pause_entry = ttk.Entry(max_pause_frame, width=6)
max_pause_entry.insert(0, "2.0")
max_pause_entry.pack(side=tk.LEFT, padx=2)

# Pause frequency
pause_freq_frame = ttk.Frame(pause_settings_frame)
pause_freq_frame.pack(side=tk.LEFT, padx=5)
pause_freq_label = ttk.Label(pause_freq_frame, text="Pause every N chars:")
pause_freq_label.pack(side=tk.LEFT)
pause_freq_entry = ttk.Entry(pause_freq_frame, width=6)
pause_freq_entry.insert(0, "50")
pause_freq_entry.pack(side=tk.LEFT, padx=2)

# Typo settings frame
typo_frame = ttk.LabelFrame(main_frame, text="Typo Settings", padding=10)
typo_frame.pack(fill=tk.X, pady=5)

# Enable typos
typo_toggle_var = tk.BooleanVar(value=True)
typo_toggle = ttk.Checkbutton(typo_frame, text="Enable random typos", variable=typo_toggle_var)
typo_toggle.pack(anchor=tk.W)

# Typo frequency
typo_freq_frame = ttk.Frame(typo_frame)
typo_freq_frame.pack(fill=tk.X, pady=5)
typo_freq_label = ttk.Label(typo_freq_frame, text="Typo chance (%):")
typo_freq_label.pack(side=tk.LEFT)
typo_freq_entry = ttk.Entry(typo_freq_frame, width=6)
typo_freq_entry.insert(0, "30")  # 30% chance by default
typo_freq_entry.pack(side=tk.LEFT, padx=2)

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)
start_button = ttk.Button(button_frame, text="Start (F9)", command=type_text)
start_button.pack(side=tk.LEFT, padx=5)
cancel_button = ttk.Button(button_frame, text="Cancel (ESC)", command=root.quit)
cancel_button.pack(side=tk.LEFT, padx=5)

# Start the custom listener in a separate thread
listener = CustomListener(on_press=on_press, daemon=True)
listener_thread = threading.Thread(target=listener.run, daemon=True)
listener_thread.start()

# Start the clipboard updater in a separate thread
clipboard_thread = threading.Thread(target=update_clipboard, daemon=True)
clipboard_thread.start()

root.mainloop()