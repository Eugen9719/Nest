from shop.models import Category


def p_categories(request):
    categories = Category.objects.prefetch_related('children').filter(parent=None)
    return {'categories': categories}