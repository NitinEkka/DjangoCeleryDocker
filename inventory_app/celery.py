from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

app = Celery('inventory_management')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_IGNORE_RESULT = False
CELERY_ALWAYS_EAGER = False
# CELERY_IGNORE_QUEUES = ('queue',)





# Production Docker

# app.congif['CELERY_BACKEND'] = "redis://redis:6379/0"
# app.config['CELERY_BROKER_URL'] = "redis://redis:6379/0"

# result = app.send_task('rocket_message_log', queue='queue1')

# app1 = Celery('inventory_management1')
# app1.conf.enable_utc = False

# app1.conf.update(timezone = 'Asia/Kolkata')
# app1.config_from_object('django.conf:settings', namespace='CELERY')
# app1.autodiscover_tasks()