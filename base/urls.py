from django.urls import path
from base import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register_user, name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='base/logout.html'), name='logout'),
    path('profile/', views.orgnization_profile, name='profile'),
    path('invoice/', views.invoice, name='invoice-form'),
    path('itemform/', views.item_test, name='item-form'),
    
]