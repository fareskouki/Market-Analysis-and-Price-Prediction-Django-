# in production/models.py
from django.db import models
from marche.models import DonneeMarche
from Climat.models import DonneeClimatique  # Import the climate data model

class Production(models.Model):
    produit_marche = models.ForeignKey(DonneeMarche, on_delete=models.CASCADE, related_name='productions')
    quantite = models.FloatField()  # Quantity produced
    date = models.DateField()  # Date of production
    region = models.CharField(max_length=255)  # Region where the production took place
    donnees_climatiques = models.ForeignKey(DonneeClimatique, on_delete=models.CASCADE, related_name='productions')

    def __str__(self):
        return f"{self.produit_marche.produit} - {self.date} - {self.quantite} tonnes"
