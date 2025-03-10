from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsport.settings')

app = Celery('newsport')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()