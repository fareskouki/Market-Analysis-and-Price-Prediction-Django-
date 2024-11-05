from django.urls import path
from . import views

urlpatterns = [
    path('', views.production_list, name='production_list'),
    path('create/', views.production_create, name='production_create'),
    path('update/<int:pk>/', views.production_update, name='production_update'),
    path('delete/<int:pk>/', views.production_delete, name='production_delete'),
]
