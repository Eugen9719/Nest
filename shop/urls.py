
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='index'),
    path('shop/', views.products_list, name='products_list'),
    path('shop/<slug:category_slug>/', views.products_list, name='products_list_by_category'),
    path('detail/<slug:product_slug>', views.product_detail, name='product_detail'),

]
