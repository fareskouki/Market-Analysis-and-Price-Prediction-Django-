from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Optional description for the category

    def __str__(self):
        return self.name


class DonneeMarche(models.Model):
    produit = models.CharField(max_length=100)
    prix_produit = models.FloatField()
    demande_produit = models.IntegerField()
    offre_produit = models.IntegerField()
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='donnees_marche')

    def __str__(self):
        return self.produit
