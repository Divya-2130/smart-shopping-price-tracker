"""
config/celery.py
-----------------
Celery lets us run a job automatically in the background on a schedule
(e.g. "check all tracked product prices every 6 hours") without a user
needing to click a button.

To run it locally, in two separate terminals:
    celery -A config worker --loglevel=info
    celery -A config beat --loglevel=info
"""
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
