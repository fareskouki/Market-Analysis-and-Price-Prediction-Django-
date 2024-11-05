import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from django.conf import settings
import os
import joblib
from marche.models import DonneeMarche

def entrainer_modele():
    # Récupérer les données du marché depuis la base de données
    donnees = DonneeMarche.objects.all().values('prix_produit', 'offre_produit', 'demande_produit')
    df = pd.DataFrame(donnees)
    
    if df.empty:
        raise ValueError("Pas assez de données pour entraîner le modèle")

    # Séparation des variables indépendantes (X) et dépendante (y)
    X = df[['offre_produit', 'demande_produit']]
    y = df['prix_produit']
    
    # Séparer les données en ensemble d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Créer et entraîner le modèle de régression linéaire
    modele = LinearRegression()
    modele.fit(X_train, y_train)
    
    # Sauvegarder le modèle
    modele_path = os.path.join(settings.BASE_DIR, 'marche', 'modele_prix.joblib')
    joblib.dump(modele, modele_path)
    print("Modèle entraîné et sauvegardé avec succès.")
