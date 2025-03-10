# newsport/newsport/__init__.py
from newsport.celery_config import app as celery_app
__all__ = ('celery_app',)