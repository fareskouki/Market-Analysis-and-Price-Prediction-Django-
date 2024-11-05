from django.urls import path
from . import views

urlpatterns = [
    path('donnee/', views.production_list, name='production_list'),
]