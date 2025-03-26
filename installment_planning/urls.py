from django.urls import path
from . import views

urlpatterns = [
    path('', views.installment_planning_view, name='installment_planning'),
]