from django.contrib import admin

# Register your models here.

# Register your models here.
from django.contrib import admin
from .models import  PrévisionPrix

# @admin.register(ProduitAgricole)
# class ProduitAgricoleAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'type_produit', 'unite_mesure', 'prix')
#     search_fields = ('nom', 'type_produit')
#     list_filter = ('type_produit',)
#     ordering = ('nom',)

@admin.register(PrévisionPrix)
class PrévisionPrixAdmin(admin.ModelAdmin):
    list_display = ('date_prevision', 'prix_prevu', 'confiance', 'methode')
    # search_fields = ('produit__nom', 'methode')
    # list_filter = ('date_prevision')
    ordering = ('-date_prevision',)
    date_hierarchy = 'date_prevision'
