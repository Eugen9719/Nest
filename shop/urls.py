
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='index'),
    path('child-categories/<int:id>/', views.child_categories, name='child_categories'),
    path('shop/<slug:category_slug>/', views.products_list_by_category, name='products_list_by_category'),
    path('detail/<slug:product_slug>', views.product_detail, name='product_detail'),

]
