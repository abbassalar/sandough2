from django.urls import path
from . import views

urlpatterns = [
    path('', views.installment_payment_view, name='installment_payment'),
]