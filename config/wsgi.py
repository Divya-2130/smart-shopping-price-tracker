"""
config/wsgi.py
---------------
Used by production servers (e.g. Gunicorn) to run the Django app.
You don't edit this for normal development.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
