from django.contrib import admin
from .models import DonneeMarche, Category

@admin.register(DonneeMarche)
class DonneeMarcheAdmin(admin.ModelAdmin):
    list_display = ('produit', 'prix_produit', 'demande_produit', 'offre_produit', 'date_enregistrement', 'category')
    search_fields = ('produit', 'category__name')  # Allow searching by product and category name

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
