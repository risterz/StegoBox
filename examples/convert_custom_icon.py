#!/usr/bin/env python3
"""
Convert the custom AI-generated icon to Windows .ico format
"""

from PIL import Image
import os

def convert_to_ico():
    """Convert the custom icon to .ico format"""
    
    # Find the firefly icon file
    icon_files = [f for f in os.listdir('.') if f.startswith('Firefly_Modern') and f.endswith('.png')]
    
    if not icon_files:
        print("❌ Custom icon file not found!")
        return False
    
    source_file = icon_files[0]
    print(f"🎨 Found custom icon: {source_file}")
    
    try:
        # Open the source image
        img = Image.open(source_file)
        print(f"📊 Original size: {img.size}")
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create different sizes for the ICO file
        sizes = [16, 32, 48, 64, 128, 256]
        icons = []
        
        for size in sizes:
            # Resize the image
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icons.append(resized)
            print(f"✅ Created {size}x{size} version")
        
        # Save as ICO file
        icons[0].save('custom_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
        print("✅ Created custom_icon.ico")
        
        # Also save a high-res PNG version
        img.save('custom_icon.png', 'PNG')
        print("✅ Created custom_icon.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting icon: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Converting Custom StegoBox Icon")
    print("=" * 40)
    
    success = convert_to_ico()
    
    if success:
        print("\n🎉 Icon conversion completed!")
        print("Files created:")
        print("• custom_icon.ico (for Windows executable)")
        print("• custom_icon.png (high-resolution version)")
    else:
        print("\n💥 Icon conversion failed!")