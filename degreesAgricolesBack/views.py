from django.shortcuts import render
from .models import degreesAgricoles

def degreesAgricolesBack(request):
    degreesAgricolesBack = degreesAgricoles.objects.all()  # Retrieve all products
    return render(request, 'degreesAgricolesBack/liste_degreesAgricoleBack.html', {'degreesAgricolesBack': degreesAgricolesBack})
