from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('customer/create/', views.create_customer_view, name='create_customer'),
    path('customer/<int:customer_id>/', views.customer_detail_view, name='customer_detail'),
    path('customer/search/', views.customer_search_view, name='customer_search'),
    path('account/create/', views.create_account_view, name='create_account'),
]