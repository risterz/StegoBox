#!/usr/bin/env python3
"""
StegoBox GUI - Advanced Steganography Tool
Main launcher script that imports the core functionality from src/
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main GUI application
try:
    from example import main as run_cli
    from gui_app import StegoBoxGUI
    import customtkinter as ctk
    
    def main():
        """Launch the StegoBox GUI application"""
        try:
            app = StegoBoxGUI()
            app.mainloop()
        except ImportError as e:
            print(f"Error importing GUI dependencies: {e}")
            print("Please install required packages: pip install -r requirements.txt")
            sys.exit(1)
    
    if __name__ == "__main__":
        main()
        
except ImportError:
    # Fallback to CLI if GUI dependencies are not available
    print("GUI dependencies not available, falling back to CLI...")
    print("To use the GUI, please install: pip install -r requirements.txt")
    if __name__ == "__main__":
        run_cli()