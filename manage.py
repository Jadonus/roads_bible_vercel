#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from subprocess import run
from django.conf import settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_bible.settings')
    try:
        from django.core.management import execute_from_command_line

        if len(sys.argv) > 1 and sys.argv[1] == 'makeimage':
            if len(sys.argv) > 2:
                # Concatenate all words after 'makeimage'
                msg = " ".join(sys.argv[2:])
                # Use the same for image name
                image_name = "".join(sys.argv[2:])
                make_image(image_name, msg)
            else:
                print("Please provide a message after 'makeimage'")
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
