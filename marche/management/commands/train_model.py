from django.core.management.base import BaseCommand
from marche.views import entrainer_modele

class Command(BaseCommand):
    help = 'Entraîne le modèle de prix'

    def handle(self, *args, **kwargs):
        try:
            entrainer_modele()
            self.stdout.write(self.style.SUCCESS('Modèle entraîné avec succès.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de l\'entraînement du modèle: {e}'))
