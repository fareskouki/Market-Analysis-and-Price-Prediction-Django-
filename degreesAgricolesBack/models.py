from django.db import models

class degreesAgricoles(models.Model):
    item = models.CharField(max_length=100, default='Sugar')
    year = models.IntegerField(verbose_name="l'annee conserner")
    value = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Prix en €", null=True, blank=True)
    area = models.CharField(max_length=100, verbose_name="le pays concerner")

    class Meta:
        verbose_name = "Sugar Agricole"
        verbose_name_plural = "sugar Agricoles"
        ordering = ['item']

    def __str__(self):
        return f"{self.item} - {self.value}"