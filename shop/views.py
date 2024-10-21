from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from cart.forms import CartAddProductForm
from shop.form import ProductReviewForm
from shop.models import Product, Category, ProductReview, Characteristic, CharacteristicValue


def home(request):
    return render(request, 'index.html')


def products_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    # Получаем уникальные атрибуты и их значения для продуктов в данной категории
    characteristics = Characteristic.objects.filter(category=category)
    unique_char = {}

    for char in characteristics:
        char_values = CharacteristicValue.objects.filter(characteristic=char, product__in=products) \
            .values('value') \
            .annotate(count=Count('value')) \
            .order_by('value')
        unique_char[char] = char_values

    # Получаем выбранные значения атрибутов из GET запроса
    selected_values = request.GET.getlist('attribute_values')

    # Формируем QuerySet для фильтрации продуктов по выбранным значениям атрибутов
    filtered_products = products
    for value in selected_values:
        filtered_products = filtered_products.filter(cvalue__value=value)

    # Получаем параметры фильтрации по цене из GET запроса
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')



    # Применяем фильтры по цене, если они заданы

    if min_price:
        filtered_products = filtered_products.filter(price__gte=min_price)
    if max_price:
        filtered_products = filtered_products.filter(price__lte=max_price)

    context = {
        'category': category,
        'products': filtered_products,  # Передаем отфильтрованные продукты
        'unique_char': unique_char,  # Передаем уникальные атрибуты в шаблон
        'category_path': category.get_category_path(),
    }
    return render(request, 'products/products-list.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    images = product.media.all()
    reviews = product.reviews.all()

    # Проверяем, может ли пользователь оставить отзыв
    make_review = not ProductReview.objects.filter(user=request.user,
                                                   product=product).exists() if request.user.is_authenticated else False

    # Обработка формы
    cart_product_form = CartAddProductForm()
    form = ProductReviewForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        return redirect(product.get_absolute_url())

    return render(request, 'products/detail-product.html', {
        'product': product,
        'images': images,
        'reviews': reviews,
        'form': form,
        'make_review': make_review,
        'cart_product_form':cart_product_form,
    })


def child_categories(request, id):
    category = get_object_or_404(Category, id=id)
    child_categories = category.children.all()

    # Если у категории нет дочерних категорий, перенаправляем на список продуктов
    if not child_categories.exists():
        return redirect('shop:products_list_by_category', category_slug=category.slug)

    context = {
        'category': category,
        'child_categories': child_categories,
        'category_path': category.get_category_path(),  # передаем путь категории
    }
    print(category.get_category_path())
    return render(request, 'products/cat.html', context)
