from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_customer_view, name='create_customer'),
    path('search/', views.customer_search_view, name='customer_search'),
    path('detail/<int:customer_id>/', views.customer_detail_view, name='customer_detail'),
]