from django.contrib import admin

from Climat.models import DonneeClimatique
from Production.models import Production

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('produit_marche', 'quantite', 'date', 'region')
    search_fields = ('produit_marche__produit', 'region')  # Allows searching by product name and region
    list_filter = ('date', 'region')  # Enables filtering by date and region
    ordering = ('-date',)  # Orders by date, newest first
    date_hierarchy = 'date'  # Adds a date hierarchy navigation
