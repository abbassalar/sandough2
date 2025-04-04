from django.urls import path
from . import views

urlpatterns = [
    path('installment-payment/<int:loan_id>/', views.installment_payment_view, name='installment_payment'),
    path('', views.loan_view, name='loan'),
    path('detail/<int:loan_id>/', views.loan_detail_view, name='loan_detail'),
]