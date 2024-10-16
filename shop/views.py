from django.shortcuts import render, get_object_or_404

from shop.models import Product


def home(request):
    return render(request, 'index.html')


def products_list(request):
    products = Product.objects.all()
    return render(request, 'products/products-list.html', {'products': products})


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'products/detail-product.html', {'product': product})
