import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal_django.settings')

app = Celery('NewsPortal_django')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_week_mon_8am': {
        'task': 'newsportalapp.tasks.weekly_news',
        # 'schedule': 59,
        # 'args': (5, ),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}