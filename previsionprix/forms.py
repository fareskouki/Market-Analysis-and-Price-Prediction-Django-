from django import forms
from .models import PrévisionPrix

class PrévisionPrixForm(forms.ModelForm):
    class Meta:
        model = PrévisionPrix
        fields = ['date_prevision', 'prix_prevu', 'confiance', 'methode']
