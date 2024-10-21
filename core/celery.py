# core/celery.py (или где у вас находится конфигурация Celery)
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Убедитесь, что используете имя сервиса RabbitMQ
app.conf.broker_url = 'amqp://admin:admin@rabbitmq:5672//'
app.autodiscover_tasks()
