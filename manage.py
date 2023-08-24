#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def make_image(image_name):
    gradient_path = os.path.join(settings.STATIC_ROOT, 'gradient.jpg')
    
    img = Image.open(gradient_path)
    
    # Convert the image to RGB mode if it's not already in RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    msg = image_name
    font = ImageFont.truetype('static/libsans.otf', 170)
    
    text_width, text_height = font.getsize(msg)
    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)
    
    x = (image_width - text_width) // 2
    y = (image_height - text_height) // 2
    
    draw.text((x, y), msg, font=font, fill=(255, 255, 255))
    
    image_path = os.path.join(settings.STATIC_ROOT, f"{image_name}.png")
    
    img.save(image_path)
    print("\033[32mImage Cretaed in /static! 👏")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_bible.settings')
    try:
        from django.core.management import execute_from_command_line
        
        if len(sys.argv) > 1 and sys.argv[1] == 'makeimage':
            if len(sys.argv) > 2:
                image_name = sys.argv[2]
                make_image(image_name)
            else:
                print("Please provide an image name after 'makeimage'")
                return
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

