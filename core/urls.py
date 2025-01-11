from django.contrib import admin
from django.urls import path
from .views import HomeTemplateView, dashboard_view, BankChurnView, process_input

urlpatterns = [
    path("", HomeTemplateView.as_view(), name='home'),
    path("bankchurn/", BankChurnView, name='bankchurn'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('process-input/', process_input, name='process_input'),
]
