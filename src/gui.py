"""
Sets up the Tkinter GUI, manages user input for typing settings,
and provides config to the typing engine.
"""

import tkinter as tk
from tkinter import ttk
import pyperclip
import time
import threading

from .typing_engine import stop_typing  # We can set stop_typing = True from GUI
# We do not import type_text directly here; we let typing_engine.start_typing_thread() handle it.

# Global references to GUI elements so we can fetch their values
root = None
text_input = None
min_speed_entry = None
max_speed_entry = None
delay_entry = None
clipboard_option_var = None
random_toggle_var = None
thinking_toggle_var = None
min_pause_entry = None
max_pause_entry = None
pause_freq_entry = None
typo_toggle_var = None
typo_freq_entry = None

def get_current_typing_config():
    """
    Collects all the current settings from GUI controls
    and returns them as a dictionary for the typing_engine.type_text function.
    """
    config = {}

    # If the GUI isn't fully initialized, return defaults
    if not all([text_input, min_speed_entry, max_speed_entry, delay_entry,
                clipboard_option_var, random_toggle_var, thinking_toggle_var,
                min_pause_entry, max_pause_entry, pause_freq_entry,
                typo_toggle_var, typo_freq_entry]):
        # Return default config if something goes wrong
        return {
            'text': "",
            'min_wpm': 40.0,
            'max_wpm': 80.0,
            'delay': 0.25,
            'thinking_enabled': True,
            'min_pause': 0.5,
            'max_pause': 2.0,
            'pause_frequency': 50,
            'typos_enabled': True,
            'typo_chance': 0.3,
            'random_letters': False
        }

    current_text = text_input.get("1.0", tk.END).strip()
    use_clipboard = clipboard_option_var.get()
    if use_clipboard:
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                current_text = clipboard_text
        except:
            pass

    config['text'] = current_text
    config['min_wpm'] = float(min_speed_entry.get())
    config['max_wpm'] = float(max_speed_entry.get())
    config['delay'] = float(delay_entry.get())
    config['thinking_enabled'] = thinking_toggle_var.get()
    config['min_pause'] = float(min_pause_entry.get())
    config['max_pause'] = float(max_pause_entry.get())
    config['pause_frequency'] = int(pause_freq_entry.get())
    config['typos_enabled'] = typo_toggle_var.get()
    config['typo_chance'] = float(typo_freq_entry.get()) / 100.0
    config['random_letters'] = random_toggle_var.get()

    return config

def update_clipboard_loop():
    """
    Periodically checks the clipboard and updates the text box if
    the 'Use clipboard text' option is selected.
    """
    while True:
        if clipboard_option_var.get():
            try:
                clipboard_text = pyperclip.paste()
                current_text = text_input.get("1.0", tk.END).strip()
                if clipboard_text and clipboard_text != current_text:
                    text_input.delete("1.0", tk.END)
                    text_input.insert("1.0", clipboard_text)
            except Exception as e:
                print(f"Error updating clipboard: {e}")
        time.sleep(1)

def run_gui():
    """
    Builds and displays the Tkinter GUI, then starts the main loop.
    """
    global root
    global text_input
    global min_speed_entry
    global max_speed_entry
    global delay_entry
    global clipboard_option_var
    global random_toggle_var
    global thinking_toggle_var
    global min_pause_entry
    global max_pause_entry
    global pause_freq_entry
    global typo_toggle_var
    global typo_freq_entry

    root = tk.Tk()
    root.title("Auto Typer")

    # Main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Text input label and box
    text_label = ttk.Label(main_frame, text="Enter text to type:")
    text_label.pack(pady=5)
    text_input = tk.Text(main_frame, height=10, width=50)
    text_input.pack(pady=5)

    # Settings frame
    settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=10)
    settings_frame.pack(fill=tk.X, pady=5)

    # Variables
    clipboard_option_var = tk.BooleanVar(value=True)
    random_toggle_var = tk.BooleanVar(value=False)
    thinking_toggle_var = tk.BooleanVar(value=True)
    typo_toggle_var = tk.BooleanVar(value=True)

    # Left column
    left_column = ttk.Frame(settings_frame)
    left_column.pack(side=tk.LEFT, padx=5)

    clipboard_option = ttk.Checkbutton(
        left_column, 
        text="Use clipboard text", 
        variable=clipboard_option_var
    )
    clipboard_option.pack(anchor=tk.W)

    random_toggle = ttk.Checkbutton(
        left_column, 
        text="Add random letters", 
        variable=random_toggle_var
    )
    random_toggle.pack(anchor=tk.W)

    # Right column for other settings
    right_column = ttk.Frame(settings_frame)
    right_column.pack(side=tk.LEFT, padx=5)

    # Typing speed entries
    speed_frame = ttk.Frame(settings_frame)
    speed_frame.pack(fill=tk.X, pady=2)

    min_speed_label = ttk.Label(speed_frame, text="Min typing speed (WPM):")
    min_speed_label.pack(side=tk.LEFT)
    min_speed_entry = ttk.Entry(speed_frame, width=8)
    min_speed_entry.insert(0, "40")
    min_speed_entry.pack(side=tk.LEFT, padx=5)

    max_speed_label = ttk.Label(speed_frame, text="Max typing speed (WPM):")
    max_speed_label.pack(side=tk.LEFT, padx=(10, 0))
    max_speed_entry = ttk.Entry(speed_frame, width=8)
    max_speed_entry.insert(0, "80")
    max_speed_entry.pack(side=tk.LEFT, padx=5)

    # Delay entry
    delay_frame = ttk.Frame(right_column)
    delay_frame.pack(fill=tk.X, pady=2)
    delay_label = ttk.Label(delay_frame, text="Start delay (sec):")
    delay_label.pack(side=tk.LEFT)
    delay_entry = ttk.Entry(delay_frame, width=8)
    delay_entry.insert(0, "0.25")
    delay_entry.pack(side=tk.LEFT, padx=5)

    # Thinking Pauses
    thinking_frame = ttk.LabelFrame(main_frame, text="Thinking Pauses", padding=10)
    thinking_frame.pack(fill=tk.X, pady=5)

    thinking_toggle = ttk.Checkbutton(
        thinking_frame, 
        text="Enable random thinking pauses", 
        variable=thinking_toggle_var
    )
    thinking_toggle.pack(anchor=tk.W)

    pause_settings_frame = ttk.Frame(thinking_frame)
    pause_settings_frame.pack(fill=tk.X, pady=5)

    min_pause_frame = ttk.Frame(pause_settings_frame)
    min_pause_frame.pack(side=tk.LEFT, padx=5)
    min_pause_label = ttk.Label(min_pause_frame, text="Min pause (sec):")
    min_pause_label.pack(side=tk.LEFT)
    min_pause_entry = ttk.Entry(min_pause_frame, width=6)
    min_pause_entry.insert(0, "0.5")
    min_pause_entry.pack(side=tk.LEFT, padx=2)

    max_pause_frame = ttk.Frame(pause_settings_frame)
    max_pause_frame.pack(side=tk.LEFT, padx=5)
    max_pause_label = ttk.Label(max_pause_frame, text="Max pause (sec):")
    max_pause_label.pack(side=tk.LEFT)
    max_pause_entry = ttk.Entry(max_pause_frame, width=6)
    max_pause_entry.insert(0, "2.0")
    max_pause_entry.pack(side=tk.LEFT, padx=2)

    pause_freq_frame = ttk.Frame(pause_settings_frame)
    pause_freq_frame.pack(side=tk.LEFT, padx=5)
    pause_freq_label = ttk.Label(pause_freq_frame, text="Pause every N chars:")
    pause_freq_label.pack(side=tk.LEFT)
    pause_freq_entry = ttk.Entry(pause_freq_frame, width=6)
    pause_freq_entry.insert(0, "50")
    pause_freq_entry.pack(side=tk.LEFT, padx=2)

    # Typo settings
    typo_frame = ttk.LabelFrame(main_frame, text="Typo Settings", padding=10)
    typo_frame.pack(fill=tk.X, pady=5)

    typo_toggle = ttk.Checkbutton(
        typo_frame, 
        text="Enable random typos", 
        variable=typo_toggle_var
    )
    typo_toggle.pack(anchor=tk.W)

    typo_freq_frame = ttk.Frame(typo_frame)
    typo_freq_frame.pack(fill=tk.X, pady=5)
    typo_freq_label = ttk.Label(typo_freq_frame, text="Typo chance (%):")
    typo_freq_label.pack(side=tk.LEFT)
    global typo_freq_entry
    typo_freq_entry = ttk.Entry(typo_freq_frame, width=6)
    typo_freq_entry.insert(0, "30")
    typo_freq_entry.pack(side=tk.LEFT, padx=2)

    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)

    def start_typing_callback():
        """
        Calls the typing engine to start typing in a separate thread.
        """
        # The hotkey (F9) also does this, but a button is convenient too
        from .typing_engine import start_typing_thread
        start_typing_thread()

    def cancel_typing_callback():
        """
        Cancel typing and close the application window.
        """
        global stop_typing
        stop_typing = True
        root.quit()

    start_button = ttk.Button(button_frame, text="Start (F9)", command=start_typing_callback)
    start_button.pack(side=tk.LEFT, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancel (ESC)", command=cancel_typing_callback)
    cancel_button.pack(side=tk.LEFT, padx=5)

    # Start the clipboard watcher
    clipboard_thread = threading.Thread(target=update_clipboard_loop, daemon=True)
    clipboard_thread.start()

    # Finally, run the main loop
    root.mainloop()
