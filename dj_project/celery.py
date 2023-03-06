import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_project.settings')

app = Celery()

app.config_from_object('django.conf:settings', namespace='CELERY')

# Загружать модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
