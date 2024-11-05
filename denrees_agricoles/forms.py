
# denrees_agricoles/forms.py
from django import forms
from .models import DenreesAgricoles
class DenreesAgricolesForm(forms.ModelForm):
    class Meta:
        model = DenreesAgricoles
        fields = '__all__'  # Inclure tous les champs du modèle
