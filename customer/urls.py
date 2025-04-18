from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_customer_view, name='create_customer'),  # نام رو به create_customer تغییر دادم
    path('search/', views.customer_search_view, name='customer_search'),
    path('detail/<int:customer_id>/', views.customer_detail_view, name='customer_detail'),
    path('edit/<int:customer_id>/', views.edit_customer_view, name='edit_customer'),
    path('send-message/<int:customer_id>/', views.send_message_view, name='send_message'),
]