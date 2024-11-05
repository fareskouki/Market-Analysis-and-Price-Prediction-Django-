from django.db import models

class DenreesAgricoles(models.Model):
    domain_code = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    area_code = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    element_code = models.CharField(max_length=100)
    element = models.CharField(max_length=100)
    item_code = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    year_code = models.IntegerField()
    year = models.IntegerField()
    months_code = models.CharField(max_length=100)
    months = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    value = models.FloatField()
    flag = models.CharField(max_length=10)
    flag_description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.item} ({self.year})"

