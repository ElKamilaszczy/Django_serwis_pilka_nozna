from django.urls import path

from . import views

urlpatterns = (
    path('', views.kluby, name='kluby'),
path('<int:id_klubu>/', views.detail, name='detail'),

)