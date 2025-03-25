# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Load environment variables
REDIS_HOST = os.environ.get('REDIS_HOST')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gporjukti_backend_v2.settings')

app = Celery('gporjukti_backend_v2')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set broker and result backend URLs based on environment variables
if REDIS_HOST:
    app.conf.broker_url = f'redis://{REDIS_HOST}:6380/0'
    app.conf.result_backend = f'redis://{REDIS_HOST}:6380/0'
elif RABBITMQ_URL:
    app.conf.broker_url = RABBITMQ_URL
    app.conf.result_backend = RABBITMQ_URL

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
