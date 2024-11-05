from django.urls import path
from . import views

urlpatterns = [
    path('', views.afficher_donnees_marche, name='afficher_donnees_marche'),
    path('analyse/', views.analyse_prix_ia, name='analyse_prix_ia'),
   path('toutes-donnees/', views.afficher_toutes_donnees_marche, name='afficher_toutes_donnees_marche'),
   path('analyse2/', views.analyse_prix_ia2, name='analyse_prix_ia2'),
]
