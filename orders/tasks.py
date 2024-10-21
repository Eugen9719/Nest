from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order




@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order #{order.id}'
    message = f'Order #{order.id} is created.'
    mail_sent = send_mail(
        subject, message, settings.EMAIL_HOST_USER, [order.email],
    )
    return mail_sent
