from django.db import models
from denrees_agricoles.models import DenreesAgricoles  # Importez DenreesAgricoles ici

class Production(models.Model):
    denree = models.ForeignKey(DenreesAgricoles, on_delete=models.CASCADE, related_name='productions')
    quantity = models.FloatField()  # Quantité produite
    year = models.IntegerField()
    description = models.TextField()  # Description de la production

    def __str__(self):
        return f"Production of {self.denree.item} in {self.year}: {self.quantity}"
