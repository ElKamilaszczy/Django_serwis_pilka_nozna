from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout, login, logout_then_login
urlpatterns = (
    path('', views.ligi, name='ligi'),
    path('<int:id_ligi>/tabela', views.tabela, name='tabela'),
    path('nowa_liga/', views.add_liga, name='add_liga'),
    path('<int:id_ligi>/ranking', views.ranking_st, name='ranking_st'),
    path('<int:id_ligi>/kolejki', views.kolejki, name='kolejki'),
    path('<int:id_ligi>/<int:id_klubu>', views.klub, name='klub'),
    #wzorzec url dla logowania i dodanie w urls.py admina
    #path('login/', views.user_login, name='login'),
    #Wzorce adresów URL dla widoków logowania i wylogowania
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),
    #Dla dashboardu dla organizatora:
    path('panel/', views.dashboard, name = 'dashboard')
)