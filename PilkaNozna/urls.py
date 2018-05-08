from django.urls import path

from . import views

urlpatterns = [
    path('', views.liga, name='liga'),
    path('', views.kluby, name='kluby'),
]