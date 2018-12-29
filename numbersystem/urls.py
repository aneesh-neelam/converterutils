from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_number_system_v1, name='api_number_system_v1'),
    path('convert/', views.api_number_system_v1_convert, name='api_number_system_v1_convert'),
]
