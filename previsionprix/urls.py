from django.urls import path
from . import views

urlpatterns = [
    path('', views.prevision_list, name='prevision_list'),
    path('prevision/<int:id>/', views.prevision_detail, name='prevision_detail'),
    path('prevision/ajouter/', views.prevision_create, name='prevision_create'),
    path('prevision/<int:id>/modifier/', views.prevision_update, name='prevision_update'),
    path('prevision/<int:id>/supprimer/', views.prevision_delete, name='prevision_delete'),
]
