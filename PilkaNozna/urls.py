from django.urls import path

from . import views

urlpatterns = (
    path('', views.ligi, name='ligi'),
    path('<int:id_ligi>/', views.detail, name='detail'),
    path('nowa_liga/', views.add_liga, name='add_liga'),
)