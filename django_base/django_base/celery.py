import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_base.settings')

app = Celery('django_base')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()