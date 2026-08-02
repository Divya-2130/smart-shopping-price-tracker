#!/usr/bin/env python
"""
manage.py
----------
This is Django's command-line utility. You run this file to:
  - start the server:        python manage.py runserver
  - create migrations:       python manage.py makemigrations
  - apply migrations:        python manage.py migrate
  - create admin user:       python manage.py createsuperuser
You normally never need to edit this file.
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
