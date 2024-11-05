
# Create your models here.
from django.db import models



class PrévisionPrix(models.Model):
    # produit = models.ForeignKey(ProduitAgricole, on_delete=models.CASCADE)
    date_prevision = models.DateField()
    prix_prevu = models.DecimalField(max_digits=10, decimal_places=2)
    confiance = models.DecimalField(max_digits=5, decimal_places=2)
    methode = models.CharField(max_length=100)

    def __str__(self):
        return  self.methode
