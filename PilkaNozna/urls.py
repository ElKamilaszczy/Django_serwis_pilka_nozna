from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout, login, logout_then_login
urlpatterns = (
    path('', views.ligi, name='ligi'),
    path('<int:id_ligi>/tabela', views.tabela, name='tabela'),
    #path('panel/nowa_liga/', views.dodaj_lige, name='dodaj_lige'),
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
    path('panel/', views.panel, name='panel'),
    path('panel/dodaj_klub/', views.dodaj_klub, name='dodaj_klub'),
    path('panel/dodaj_mecz/', views.dodaj_mecz, name = 'dodaj_mecz'),
    path('panel/dodaj_statystyki/', views.dodaj_statystyki, name = 'dodaj_statystyki'),
    path('panel/dodaj_pilkarza/', views.dodaj_pilkarza, name = 'dodaj_pilkarza'),
    path('panel/dodaj_lige/', views.dodaj_lige, name = 'dodaj_lige'),
    path('panel/wyslij_wiadomosc/', views.wyslij_wiadomosc, name='wyslij_wiadomosc'),
)