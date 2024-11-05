from django.db import models
from marche.models import DonneeMarche

class DonneeClimatique(models.Model):
    produit_marche = models.ForeignKey(DonneeMarche, on_delete=models.CASCADE, related_name='donnees_climatiques')
    date = models.DateField()
    temperature = models.FloatField()
    precipitations = models.FloatField()
    region = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.produit_marche.produit} - {self.date}"
