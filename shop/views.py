from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from shop.form import ProductReviewForm
from shop.models import Product, Category, ProductReview


def home(request):
    return render(request, 'index.html')


def products_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'products/products-list.html',
                  {'products': products, 'category': category, 'categories': categories})


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    images = product.media.all()
    reviews = product.reviews.all()

    # Проверяем, можно ли пользователю оставить отзыв
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)  # Сохраняем, но не отправляем в базу данных сразу
            review.product = product
            review.user = request.user  # Привязываем отзыв к текущему пользователю
            review.save()  # Сохраняем отзыв в базе данных
            return redirect(product.get_absolute_url())  # Перенаправление после успешного сохранения
    else:
        form = ProductReviewForm()

    return render(request, 'products/detail-product.html',
                  {'product': product, 'images': images, 'reviews': reviews, 'form': form, 'make_review': make_review,})


def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)  # Сохраняем, но не отправляем в базу данных сразу
            review.product = product
            review.user = request.user  # Привязываем отзыв к текущему пользователю
            review.save()  # Сохраняем отзыв в базе данных
            return redirect(product.get_absolute_url())  # Перенаправление после успешного сохранения
    else:
        form = ProductReviewForm()
    return render(request, 'products/detail-product.html', {'product': product, 'form': form})
