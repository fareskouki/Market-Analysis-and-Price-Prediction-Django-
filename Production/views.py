from django.shortcuts import render
from .models import Production  # Ensure the model is correctly imported

# View to display the list of Production entries
def production_list(request):
    # Fetch all Production entries
    productions = Production.objects.all()

    # Pass the data to the template
    return render(request, 'production/production_list.html', {'productions': productions})
