from django.urls import path

from . import views, webhooks

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
