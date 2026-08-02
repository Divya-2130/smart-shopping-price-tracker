# This file makes 'config' a Python package.
# It also loads Celery so background jobs (price checking) work when Django starts.
from .celery import app as celery_app

__all__ = ("celery_app",)
