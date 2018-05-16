from django.urls import path

from . import views

urlpatterns = (
    path('', views.ligi, name='ligi'),
    path('<int:id_ligi>/tabela', views.tabela, name='tabela'),
    path('nowa_liga/', views.add_liga, name='add_liga'),
    path('<int:id_ligi>/ranking', views.ranking_st, name='ranking_st'),
    path('<int:id_ligi>/kolejki', views.kolejki, name='kolejki'),
    path('<int:id_ligi>/<int:id_klubu>', views.klub, name='klub'),

)