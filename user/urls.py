# user/urls.py

from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
]
