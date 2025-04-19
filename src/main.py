"""
Main entry point for the AutoTyper application.
Handles overall startup, subscription checks (placeholder),
and launches the GUI.
"""

import threading
from . import gui
from . import typing_engine
from . import keyboard_utils

# Placeholder for a future subscription verification mechanism
def verify_subscription():
    """
    Placeholder function for subscription verification.
    In a real implementation, this would check with a web service
    to ensure the user is authorized.
    """
    # TODO: Implement actual subscription check logic
    return True

def main():
    """
    Main startup function. Verifies subscription (placeholder) then runs the GUI.
    """
    # Subscription check (placeholder)
    if not verify_subscription():
        print("Subscription not valid. Exiting application.")
        return
    
    # Initialize the global listener in its own thread
    listener_thread = threading.Thread(
        target=keyboard_utils.start_listener, 
        daemon=True
    )
    listener_thread.start()
    
    # Run the GUI
    gui.run_gui()

# Standard Python convention for script entry
if __name__ == "__main__":
    main()
