from shop.models import Category, Wishlist


def p_categories(request):
    categories = Category.objects.prefetch_related('children').filter(parent=None)
    return {'categories': categories}


def wishlist_count(request):
    return {'wishlist_count': Wishlist.objects.filter(user=request.user).count()}
