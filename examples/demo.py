#!/usr/bin/env python3
"""
StegoBox Demo Script
Demonstrates the steganography functionality with sample data
"""

import os
import sys
from pathlib import Path
import tempfile
import shutil
from PIL import Image, ImageDraw

# Import our steganography functions
from example import (
    zip_folder_to_bytes, append_embed, append_extract,
    lsb_embed, lsb_extract, lsb_capacity
)

def create_sample_image(size=(1920, 1080), name="sample_cover.png"):
    """Create a sample cover image for testing"""
    print(f"🖼️  Creating sample image: {name}")
    
    img = Image.new('RGB', size, color=(70, 130, 180))  # Steel blue
    draw = ImageDraw.Draw(img)
    
    # Add some visual elements to make it interesting
    # Grid pattern
    grid_size = 50
    for x in range(0, size[0], grid_size):
        draw.line([(x, 0), (x, size[1])], fill=(100, 150, 200), width=1)
    for y in range(0, size[1], grid_size):
        draw.line([(0, y), (size[0], y)], fill=(100, 150, 200), width=1)
    
    # Some shapes
    draw.ellipse([size[0]//4, size[1]//4, 3*size[0]//4, 3*size[1]//4], 
                fill=(255, 255, 255, 50), outline=(255, 255, 255))
    
    # Text
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
        text = "StegoBox Demo Image"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((size[0]//2 - text_width//2, size[1]//2), text, 
                 fill=(255, 255, 255), font=font)
    except:
        pass
    
    img.save(name, "PNG")
    print(f"✅ Created {name} ({size[0]}x{size[1]})")
    return name

def create_sample_data():
    """Create sample data to hide"""
    print("📁 Creating sample secret data...")
    
    # Create temporary directory for sample data
    sample_dir = "demo_secret_data"
    if os.path.exists(sample_dir):
        shutil.rmtree(sample_dir)
    os.makedirs(sample_dir)
    
    # Create various sample files
    files_to_create = {
        "secret_message.txt": "This is a top-secret message hidden using StegoBox!\n" +
                             "The message was embedded using advanced steganography techniques.\n" +
                             "Only those who know the password can read this content.",
        
        "mission_briefing.md": """# Mission Briefing - Operation StegoBox

## Objective
Demonstrate the power of modern steganography techniques.

## Tools Used
- **StegoBox**: Advanced steganography tool
- **LSB Method**: Least Significant Bit embedding
- **AES-256 Encryption**: Military-grade security

## Success Metrics
- ✅ Data hidden successfully
- ✅ Image appears normal
- ✅ Data extracted correctly
- ✅ Encryption working properly

## Classification: TOP SECRET
""",
        
        "data.json": """{
    "project": "StegoBox",
    "version": "1.0",
    "features": [
        "LSB Steganography",
        "Append Method",
        "AES-256 Encryption",
        "Modern GUI",
        "Batch Processing"
    ],
    "supported_formats": ["PNG", "BMP", "JPEG"],
    "security_level": "Military Grade"
}""",
        
        "coordinates.csv": """Location,Latitude,Longitude,Description
Safe House Alpha,40.7128,-74.0060,Primary extraction point
Data Drop Beta,34.0522,-118.2437,Secondary communication hub
Command Center,51.5074,-0.1278,Main operations base
Backup Site,48.8566,2.3522,Emergency fallback location"""
    }
    
    # Create subdirectory
    docs_dir = os.path.join(sample_dir, "classified_docs")
    os.makedirs(docs_dir)
    
    for filename, content in files_to_create.items():
        filepath = os.path.join(docs_dir if filename.endswith(('.md', '.json')) else sample_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Created sample data in '{sample_dir}' folder")
    return sample_dir

def demo_append_method():
    """Demonstrate append method"""
    print("\n" + "="*50)
    print("🔗 DEMO: Append Method (Fast & Simple)")
    print("="*50)
    
    # Create sample image and data
    cover_image = create_sample_image((800, 600), "append_cover.png")
    secret_data = create_sample_data()
    
    # Show original file size
    original_size = os.path.getsize(cover_image)
    print(f"📊 Original image size: {original_size:,} bytes")
    
    try:
        # Embed data
        print("🔒 Embedding secret data using append method...")
        payload = zip_folder_to_bytes(secret_data)
        stego_path = "append_stego.png" 
        append_embed(cover_image, payload, stego_path)
        
        # Show new file size
        stego_size = os.path.getsize(stego_path)
        print(f"📊 Stego image size: {stego_size:,} bytes (+{stego_size-original_size:,} bytes)")
        print(f"✅ Data embedded successfully: {stego_path}")
        
        # Extract data
        print("🔓 Extracting hidden data...")
        extracted_zip = "append_extracted.zip"
        append_extract(stego_path, extracted_zip)
        print(f"✅ Data extracted successfully: {extracted_zip}")
        
        # Verify extraction
        extracted_size = os.path.getsize(extracted_zip)
        print(f"📊 Extracted ZIP size: {extracted_size:,} bytes")
        
        print("🎉 Append method demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Append method demo failed: {e}")
    
    finally:
        # Cleanup
        cleanup_files = [secret_data, cover_image]
        for item in cleanup_files:
            if os.path.exists(item):
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                except (PermissionError, OSError):
                    # File might be in use, skip cleanup
                    pass

def demo_lsb_method():
    """Demonstrate LSB method with encryption"""
    print("\n" + "="*50) 
    print("🔐 DEMO: LSB Method (Stealth + Encryption)")
    print("="*50)
    
    # Create larger image for LSB capacity
    cover_image = create_sample_image((1920, 1080), "lsb_cover.png")
    secret_data = create_sample_data()
    
    # Show capacity information
    img = Image.open(cover_image)
    capacity = lsb_capacity(img)
    capacity_mb = capacity / 8 / 1024 / 1024
    print(f"📊 LSB capacity: {capacity:,} bits (~{capacity_mb:.2f} MB)")
    
    # Show original file sizes
    original_size = os.path.getsize(cover_image)
    print(f"📊 Original image size: {original_size:,} bytes")
    
    try:
        # Embed data with password
        print("🔒 Embedding secret data using LSB method with encryption...")
        payload = zip_folder_to_bytes(secret_data)
        print(f"📊 Payload size: {len(payload):,} bytes")
        
        password = "Demo_Password_2024!"
        stego_path = "lsb_stego.png"
        lsb_embed(cover_image, payload, stego_path, password=password)
        
        # Show stego image size (should be same as original)
        stego_size = os.path.getsize(stego_path)
        print(f"📊 Stego image size: {stego_size:,} bytes (difference: {stego_size-original_size:,} bytes)")
        print(f"✅ Data embedded successfully: {stego_path}")
        print(f"🔑 Password used: {password}")
        
        # Extract data
        print("🔓 Extracting hidden data with password...")
        extracted_zip = "lsb_extracted.zip"
        lsb_extract(stego_path, extracted_zip, password=password)
        print(f"✅ Data extracted successfully: {extracted_zip}")
        
        # Verify extraction
        extracted_size = os.path.getsize(extracted_zip)
        print(f"📊 Extracted ZIP size: {extracted_size:,} bytes")
        
        # Test wrong password
        print("🧪 Testing wrong password...")
        try:
            lsb_extract(stego_path, "wrong_password_test.zip", password="wrong_password")
            print("❌ Should have failed with wrong password!")
        except Exception:
            print("✅ Correctly rejected wrong password")
        
        print("🎉 LSB method demo completed successfully!")
        
    except Exception as e:
        print(f"❌ LSB method demo failed: {e}")
    
    finally:
        # Cleanup
        cleanup_files = [secret_data, cover_image]
        for item in cleanup_files:
            if os.path.exists(item):
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                except (PermissionError, OSError):
                    # File might be in use, skip cleanup
                    pass

def show_comparison():
    """Show comparison between methods"""
    print("\n" + "="*50)
    print("📊 METHOD COMPARISON")
    print("="*50)
    
    comparison_table = """
┌─────────────────┬─────────────────┬─────────────────┐
│     Feature     │   Append Mode   │    LSB Mode     │
├─────────────────┼─────────────────┼─────────────────┤
│ Speed           │ Very Fast       │ Moderate        │
│ Stealth         │ Low             │ Very High       │
│ File Size       │ Increases       │ Same            │
│ Detection       │ Easy            │ Very Difficult  │
│ Capacity        │ Unlimited       │ Image Dependent │
│ Encryption      │ No              │ Yes (Optional)  │
│ Image Format    │ Any             │ PNG/BMP Best    │
│ Robustness      │ High            │ Moderate        │
└─────────────────┴─────────────────┴─────────────────┘
"""
    print(comparison_table)
    
    print("\n💡 RECOMMENDATIONS:")
    print("• Use APPEND for large files or maximum compatibility")
    print("• Use LSB for stealth operations and sensitive data")
    print("• Always use passwords with LSB for maximum security")
    print("• Test extraction immediately after embedding")

def main():
    """Run the complete demo"""
    print("🕵️ StegoBox Steganography Demo")
    print("🎯 Demonstrating both embedding methods")
    print("=" * 60)
    
    # Check if required modules are available
    try:
        from example import lsb_embed, append_embed
        print("✅ StegoBox modules loaded successfully")
    except ImportError as e:
        print(f"❌ Could not import StegoBox modules: {e}")
        print("Make sure example.py is in the same directory")
        sys.exit(1)
    
    # Run demos
    demo_append_method()
    demo_lsb_method()
    show_comparison()
    
    # Show generated files
    print("\n📁 Generated demo files:")
    demo_files = [
        "append_stego.png", "append_extracted.zip",
        "lsb_stego.png", "lsb_extracted.zip"
    ]
    
    for file in demo_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   • {file} ({size:,} bytes)")
    
    print("\n🎉 Demo completed! You can now:")
    print("1. Examine the stego images (they look normal!)")
    print("2. Extract the ZIP files to see the hidden data")
    print("3. Try the GUI version: python stegobox_gui.py")
    
    # Cleanup option
    response = input("\n🧹 Clean up demo files? [y/N]: ").strip().lower()
    if response == 'y':
        for file in demo_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  Removed {file}")
        print("✅ Cleanup completed")

if __name__ == "__main__":
    main()