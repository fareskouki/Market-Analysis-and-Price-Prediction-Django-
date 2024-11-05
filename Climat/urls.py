from django.urls import path
from . import views

urlpatterns = [
    path('donnees/', views.donnee_climatique_list, name='donnee_climatique_list'),
]