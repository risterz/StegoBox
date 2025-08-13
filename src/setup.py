#!/usr/bin/env python3
"""
StegoBox Setup Script
Automates the complete setup process for StegoBox
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    requirements = [
        "Pillow==10.4.0",
        "cryptography==43.0.0", 
        "customtkinter==5.2.2"
    ]
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def create_icon():
    """Create application icon"""
    print("🎨 Creating application icon...")
    try:
        subprocess.check_call([sys.executable, "create_icon.py"])
        print("✅ Icon created successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Could not create icon, continuing without it")
        return False

def test_gui():
    """Test if GUI can be imported and run"""
    print("🧪 Testing GUI components...")
    try:
        # Test imports
        import customtkinter
        import PIL
        from cryptography.fernet import Fernet
        print("✅ All GUI components working")
        return True
    except ImportError as e:
        print(f"❌ GUI test failed: {e}")
        return False

def build_executable():
    """Build the executable"""
    response = input("🔨 Build Windows executable? [y/N]: ").strip().lower()
    
    if response == 'y':
        print("Building executable...")
        try:
            subprocess.check_call([sys.executable, "build.py"])
            print("✅ Executable built successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Build failed")
            return False
    else:
        print("⏭️  Skipping executable build")
        return True

def create_sample_data():
    """Create sample data for testing"""
    print("📁 Creating sample test data...")
    
    # Create test folder
    test_folder = Path("test_data")
    test_folder.mkdir(exist_ok=True)
    
    # Create sample files
    (test_folder / "sample.txt").write_text("This is a secret message hidden in an image!")
    (test_folder / "secret.txt").write_text("StegoBox - Advanced Steganography Tool\n" + "="*40)
    
    # Create a subfolder
    subfolder = test_folder / "docs"
    subfolder.mkdir(exist_ok=True)
    (subfolder / "readme.txt").write_text("Hidden documentation file")
    
    print("✅ Sample test data created in 'test_data' folder")

def main():
    """Main setup process"""
    print("🕵️ StegoBox Setup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if we're in the right directory
    required_files = ["stegobox_gui.py", "example.py", "requirements.txt"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please run this script from the StegoBox directory")
        sys.exit(1)
    
    print("✅ All required files found")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Test GUI components
    if not test_gui():
        print("❌ GUI test failed")
        sys.exit(1)
    
    # Create icon
    create_icon()
    
    # Create sample data
    create_sample_data()
    
    # Build executable (optional)
    build_executable()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the GUI: python stegobox_gui.py")
    print("2. Test with sample data in 'test_data' folder")
    
    if Path("dist/StegoBox.exe").exists():
        print("3. Share the executable: dist/StegoBox.exe")
    
    # Ask if user wants to launch GUI
    response = input("\n🚀 Launch StegoBox GUI now? [y/N]: ").strip().lower()
    if response == 'y':
        try:
            subprocess.Popen([sys.executable, "stegobox_gui.py"])
            print("✅ GUI launched!")
        except Exception as e:
            print(f"❌ Could not launch GUI: {e}")
            print("You can manually run: python stegobox_gui.py")

if __name__ == "__main__":
    main()