from django.urls import path
from . import views

urlpatterns = [
    path('', views.loan_view, name='loan'),
]