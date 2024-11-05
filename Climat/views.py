from django.shortcuts import render
from .models import DonneeClimatique

# View to display the list of DonneeClimatique entries
def donnee_climatique_list(request):
    # Fetch all DonneeClimatique entries
    donnees = DonneeClimatique.objects.all()

    # Pass the data to the template
    return render(request, 'climat/donnee_climatique_list.html', {'donnees': donnees})