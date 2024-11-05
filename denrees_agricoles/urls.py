# denrees_agricoles/urls.py
from django.urls import path
from .views import create_denree, list_denrees, update_denree, delete_denree, import_csv ,chart_view , import_csv_chart , forecast_prices
from . import views  # Import de views


urlpatterns = [
    path('create/', create_denree, name='create_denree'),
    path('', list_denrees, name='list_denrees'),
    path('update/<int:id>/', update_denree, name='update_denree'),
    path('delete/<int:id>/', delete_denree, name='delete_denree'),
  path('import-csv/', import_csv, name='import_csv'),  # Ajoutez cette ligne
 path('import-csv-chart/', views.import_csv_chart, name='import_csv_chart'),
    path('chart/', views.chart_view, name='chart_view'),
    path('forecast/', views.forecast_prices, name='forecast_prices'),
 
]
