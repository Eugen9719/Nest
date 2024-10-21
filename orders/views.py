from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from decimal import Decimal
import stripe
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from cart.cart import Cart
from orders.tasks import order_created

stripe.api_key = settings.STRIPE_SECRET_KEY


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            order_created.delay(order.id)

            # Логика Stripe для создания сессии оплаты
            success_url = request.build_absolute_uri(reverse('orders:completed'))
            cancel_url = request.build_absolute_uri(reverse('orders:canceled'))

            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }

            for item in order.items.all():
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name
                        },
                    },
                    'quantity': item.quantity,
                })

            session = stripe.checkout.Session.create(**session_data)

            return redirect(session.url, code=303)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,

            }

        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/order/create.html', {'form': form, 'cart': cart})


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
