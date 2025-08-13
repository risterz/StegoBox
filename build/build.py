#!/usr/bin/env python3
"""
Build script for StegoBox GUI
Creates a standalone Windows executable using PyInstaller
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_exe():
    """Create the executable"""
    print("🔨 Building StegoBox.exe...")
    
    # Change to project root directory
    os.chdir("..")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                       # Single file executable
        "--windowed",                      # No console window
        "--name", "StegoBox",             # Executable name
        "--add-data", "src/example.py;src",  # Include the steganography module
        "--add-data", "src/gui_app.py;src",  # Include the GUI module
        "--add-data", "src/requirements.txt;src",  # Include requirements
        "stegobox_gui.py"                 # Main script
    ]
    
    # Use custom icon if available, otherwise fallback to generated icon
    if Path("assets/custom_icon.ico").exists():
        cmd.extend(["--icon", "assets/custom_icon.ico"])
        cmd.extend(["--version-file", "build/version_info.txt"])  # Add version info for better icon display
        print("🎨 Using custom AI-generated icon with version info")
    elif Path("icon.ico").exists():
        cmd.extend(["--icon", "icon.ico"])
        print("🎨 Using generated icon")
    else:
        print("⚠️  No icon found, building without icon")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Build successful!")
        print(f"📁 Executable created: {Path('dist/StegoBox.exe').absolute()}")
        
        # Clean up build files
        import shutil
        if Path("build").exists():
            shutil.rmtree("build")
            print("🧹 Cleaned up build directory")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
        
    return True

def main():
    print("🕵️ StegoBox Build Script")
    print("=" * 30)
    
    # Check if we're in the build directory and navigate to project root
    if Path("../stegobox_gui.py").exists():
        os.chdir("..")
    
    # Check if we're in the right directory now
    if not Path("stegobox_gui.py").exists():
        print("❌ stegobox_gui.py not found in project root")
        print("Please run this script from the StegoBox/build directory")
        sys.exit(1)
    
    if not Path("src/example.py").exists():
        print("❌ src/example.py not found")
        print("Please ensure the project structure is correct")
        sys.exit(1)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create executable
    success = create_exe()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("You can now distribute dist/StegoBox.exe")
    else:
        print("\n💥 Build failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()