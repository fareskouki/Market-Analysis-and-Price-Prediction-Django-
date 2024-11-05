from django.contrib import admin
from .models import degreesAgricoles

@admin.register(degreesAgricoles)
class DegreesAgricoleAdmin(admin.ModelAdmin):
    list_display = ('item', 'year', 'value', 'area')  # Update these to match your model fields
    search_fields = ('item', 'year', 'area')  # Adjust as needed
    list_filter = ('year', 'area')  # Adjust as needed
    ordering = ('item',)
    fields = ('item', 'year', 'value', 'area')  # Ensure these match your model fields
