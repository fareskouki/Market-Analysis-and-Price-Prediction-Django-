from django.contrib import admin
from .models import News,InflationData

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'pdf_file')
    search_fields = ('title', 'description')
    list_filter = ('date_published',)

@admin.register(InflationData)
class InflationDataAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')

