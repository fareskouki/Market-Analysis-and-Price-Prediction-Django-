from django.urls import path
from . import views

urlpatterns = [
    path('', views.degreesAgricolesBack, name='liste_degreesAgricoleBack'),  # Ensure this matches
]
