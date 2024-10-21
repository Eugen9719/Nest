
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='index'),
    path('child-categories/<int:id>/', views.child_categories, name='child_categories'),
    path('shop/<slug:category_slug>/', views.products_list_by_category, name='products_list_by_category'),
    path('detail/<slug:product_slug>', views.product_detail, name='product_detail'),

    path('wishlist/',views.wishlist, name='wishlist' ),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_wishlist, name='remove_wishlist'),

]
