
# denrees_agricoles/forms.py
from django import forms
from .models import Production

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['denree', 'quantity', 'year', 'description']
