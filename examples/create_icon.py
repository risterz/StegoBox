#!/usr/bin/env python3
"""
Creates a simple icon for StegoBox application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=256):
    """Create a simple but attractive icon for StegoBox"""
    
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Color scheme - modern gradient-like colors
    bg_color = (45, 55, 72, 255)      # Dark blue-gray
    accent_color = (59, 130, 246, 255)  # Blue
    text_color = (255, 255, 255, 255)   # White
    
    # Draw background circle with gradient effect
    margin = size // 10
    circle_bbox = [margin, margin, size - margin, size - margin]
    
    # Create gradient effect with multiple circles
    center_x, center_y = size // 2, size // 2
    max_radius = (size - 2 * margin) // 2
    
    for i in range(max_radius, 0, -2):
        alpha = int(255 * (max_radius - i) / max_radius)
        color = (*bg_color[:3], min(255, alpha + 50))
        draw.ellipse([center_x - i, center_y - i, center_x + i, center_y + i], 
                    fill=color, outline=None)
    
    # Draw main circle
    draw.ellipse(circle_bbox, fill=bg_color, outline=accent_color, width=3)
    
    # Draw spy/detective icon elements
    # Draw magnifying glass
    glass_size = size // 4
    glass_x = center_x - glass_size // 2
    glass_y = center_y - glass_size // 2 - size // 10
    
    # Magnifying glass circle
    draw.ellipse([glass_x, glass_y, glass_x + glass_size, glass_y + glass_size], 
                outline=accent_color, width=4, fill=(255, 255, 255, 50))
    
    # Handle of magnifying glass
    handle_start = (glass_x + glass_size * 0.8, glass_y + glass_size * 0.8)
    handle_end = (glass_x + glass_size * 1.3, glass_y + glass_size * 1.3)
    draw.line([handle_start, handle_end], fill=accent_color, width=4)
    
    # Draw hidden data representation (small squares/pixels)
    pixel_size = 3
    for i in range(3):
        for j in range(3):
            x = center_x - pixel_size * 1.5 + i * pixel_size + size // 8
            y = center_y + j * pixel_size + size // 8
            color = accent_color if (i + j) % 2 == 0 else text_color
            draw.rectangle([x, y, x + pixel_size - 1, y + pixel_size - 1], fill=color)
    
    # Add text "SB" for StegoBox
    try:
        # Try to use a nice font
        font_size = size // 6
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "SB"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center_x - text_width // 2
    text_y = center_y + size // 6
    
    # Draw text with shadow effect
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 128))
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    return img

def main():
    """Create icon files in multiple sizes"""
    print("🎨 Creating StegoBox icon...")
    
    # Create icons in different sizes
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        icon = create_icon(size)
        filename = f"icon_{size}x{size}.png"
        icon.save(filename, "PNG")
        print(f"✅ Created {filename}")
    
    # Create ICO file for Windows
    try:
        # Create multi-size ICO
        icons = [create_icon(size) for size in [16, 32, 48, 64, 128, 256]]
        icons[0].save("icon.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print("✅ Created icon.ico")
    except Exception as e:
        print(f"⚠️  Could not create ICO file: {e}")
        print("Using largest PNG as fallback...")
        create_icon(256).save("icon.png", "PNG")
    
    print("🎉 Icon creation completed!")

if __name__ == "__main__":
    main()