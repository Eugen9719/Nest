from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_add(request, product_id):
    """Добавление товара в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override_quantity'])

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Отображение корзины"""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override_quantity': True
        })

    return render(request, 'cart/detail.html', {'cart': cart})
