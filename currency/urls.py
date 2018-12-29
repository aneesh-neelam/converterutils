from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_currency_v1, name='api_currency_v1'),
    path('convert/', views.api_currency_v1_convert, name='api_currency_v1_convert'),
]
