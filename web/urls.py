from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api, name='api'),
    path('api/v1/', views.api_v1, name='api_v1'),
    path('api/v1/currency/', views.api_currency_v1, name='api_currency_v1'),
]
