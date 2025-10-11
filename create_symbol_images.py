#!/usr/bin/env python
import os
from PIL import Image, ImageDraw, ImageFont
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
django.setup()

from maps.models import CustomSymbol

def create_placeholder_images():
    """Create placeholder images for custom symbols"""

    # Create symbols directory if it doesn't exist
    symbols_dir = os.path.join('media', 'symbols')
    os.makedirs(symbols_dir, exist_ok=True)

    # Get existing symbols without images
    symbols = CustomSymbol.objects.filter(image='')

    for symbol in symbols:
        # Create a simple colored square with text
        img = Image.new('RGB', (64, 64), color='#4CAF50')
        draw = ImageDraw.Draw(img)

        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        # Draw text (first 2 letters of name)
        text = symbol.name[:2].upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (64 - text_width) // 2
        y = (64 - text_height) // 2

        draw.text((x, y), text, fill='white', font=font)

        # Save image
        filename = f"{symbol.name.lower().replace(' ', '_')}.png"
        filepath = os.path.join(symbols_dir, filename)
        img.save(filepath)

        # Update symbol with image path
        symbol.image = f"symbols/{filename}"
        symbol.save()

        print(f"Created image for: {symbol.name} -> {filepath}")

if __name__ == '__main__':
    create_placeholder_images()