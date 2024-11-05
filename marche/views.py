from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import DonneeMarche
import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from django.conf import settings
import numpy as np

from django.contrib.auth.decorators import login_required, user_passes_test


from django.shortcuts import render
import os
import pandas as pd
from django.conf import settings

def afficher_donnees_marche(request):
    # Charger les données
    file_path = os.path.join(settings.BASE_DIR, 'Classeur1.xlsx')
    if not os.path.exists(file_path):
        return render(request, 'marche/afficher_donnees.html', {'error': 'File not found.'})

    df = pd.read_excel(file_path)

    if df.empty:
        return render(request, 'marche/afficher_donnees.html', {'donnees': [], 'error': 'No data available.'})

    donnees = df.to_dict(orient='records')

    # Diviser les données en deux moitiés
    mid_index = len(donnees) // 2
    donnees_part1 = donnees[:mid_index]
    donnees_part2 = donnees[mid_index:]

    return render(request, 'marche/afficher_donnees.html', {
        'donnees_part1': donnees_part1,
        'donnees_part2': donnees_part2
    })
from .models import DonneeMarche
# Vérifie si l'utilisateur est admin ou superadmin
def is_admin_or_superadmin(user):
    return user.role in ['admin', 'superadmin']

@login_required
@user_passes_test(is_admin_or_superadmin)
def afficher_toutes_donnees_marche(request):
    # Retrieve all data from DonneeMarche
    donnees = DonneeMarche.objects.all()

    # Check if there are no records
    if not donnees.exists():
        return render(request, 'marche/afficher_toutes_donnees.html', {'donnees': [], 'error': 'Aucune donnée disponible.'})

    return render(request, 'marche/afficher_toutes_donnees.html', {'donnees': donnees})


def entrainer_modele():
    # Load data from the Excel file
    file_path = os.path.join(settings.BASE_DIR, 'Classeur1.xlsx')
    df = pd.read_excel(file_path)

    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("Not enough data to train the model.")

    # Select relevant columns
    df = df[['Production (Supply, liters)', 'Exports (Demand, liters)', 'Price per ton (TND)']]
    df.columns = ['offre_produit', 'demande_produit', 'prix_produit']  # Rename columns for consistency

    # Convert the columns to string to ensure .str accessor works
    df['offre_produit'] = df['offre_produit'].astype(str).str.replace(',', '')
    df['demande_produit'] = df['demande_produit'].astype(str).str.replace(',', '')
    df['prix_produit'] = df['prix_produit'].astype(str).str.replace(',', '')

    # Convert cleaned strings to float
    df['offre_produit'] = pd.to_numeric(df['offre_produit'], errors='coerce')
    df['demande_produit'] = pd.to_numeric(df['demande_produit'], errors='coerce')
    df['prix_produit'] = pd.to_numeric(df['prix_produit'], errors='coerce')

    # Remove any rows with NaN values (in case of conversion failure)
    df.dropna(inplace=True)

    # Remove outliers if necessary
    q_low = df["prix_produit"].quantile(0.01)
    q_hi = df["prix_produit"].quantile(0.99)
    df_filtered = df[(df["prix_produit"] < q_hi) & (df["prix_produit"] > q_low)]

    # Separate independent (X) and dependent (y) variables
    X = df_filtered[['offre_produit', 'demande_produit']]
    y = df_filtered['prix_produit']

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Create and train the linear regression model
    modele = LinearRegression()
    modele.fit(X_train, y_train)

    # Check the model score
    print(f"Model score: {modele.score(X_test, y_test)}")

    # Save the model and scaler
    modele_path = os.path.join(settings.BASE_DIR, 'marche', 'modele_prix.joblib')
    joblib.dump(modele, modele_path)

    scaler_path = os.path.join(settings.BASE_DIR, 'marche', 'scaler.joblib')
    joblib.dump(scaler, scaler_path)

    print("Model and scaler trained and saved successfully.")


def analyse_prix_ia(request):
    modele_path = os.path.join(settings.BASE_DIR, 'marche', 'modele_prix.joblib')
    scaler_path = os.path.join(settings.BASE_DIR, 'marche', 'scaler.joblib')

    # Load the linear regression model
    if not os.path.exists(modele_path) or not os.path.exists(scaler_path):
        return render(request, 'marche/analyses.html', {
            'message': "The AI model or scaler has not yet been trained."
        })
    
    modele = joblib.load(modele_path)
    scaler = joblib.load(scaler_path)

    # Load data from the Excel file
    file_path = os.path.join(settings.BASE_DIR, 'Classeur1.xlsx')

    # Check if the file exists again
    if not os.path.exists(file_path):
        return render(request, 'marche/analyses.html', {
            'message': f"The file {file_path} does not exist."
        })

    df = pd.read_excel(file_path, header=0)  # Ensure first row is headers

    # Print the DataFrame and columns for debugging
    print("DataFrame content:")
    print(df.head())  # Display the first few rows of the DataFrame
    print("Column names:", df.columns.tolist())  # Print the column names

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Check if 'Produit' column exists
    if 'Produit' not in df.columns:
        return render(request, 'marche/analyses.html', {
            'message': "The 'Produit' column is not found in the data."
        })

    # Filter the DataFrame for the year 2023
    df_2023 = df[df['Year'] == 2023]

    # Check if there is data for 2023
    if df_2023.empty:
        return render(request, 'marche/analyses.html', {
            'message': "No data available for the year 2023."
        })

    resultats = []

    for index, row in df_2023.iterrows():
        # Clean and prepare data for prediction
        production = str(row['Production (Supply, liters)']).replace(',', '').strip()
        exports = str(row['Exports (Demand, liters)']).replace(',', '').strip()

        # Convert to float, if the conversion fails, you might want to handle it gracefully
        try:
            X_nouvelle = [[float(production), float(exports)]]
        except ValueError as e:
            return render(request, 'marche/analyses.html', {
                'message': f"Error converting data to float: {e}"
            })

        # Make a prediction using the trained model
        prix_predit = modele.predict(scaler.transform(X_nouvelle))[0]  # Scale the new data
        prix_predit = round(prix_predit, 2)

        # Store results
        resultats.append({
            'produit': row['Produit'],  # Now this should work
            'prix_predit': prix_predit,
            'nouvelle_demande': exports,
            'nouvelle_offre': production
        })

    return render(request, 'marche/analyses.html', {
        'resultats': resultats
    })
def entrainer_modele2():
    # Retrieve market data from the database
    donnees = DonneeMarche.objects.all().values('prix_produit', 'offre_produit', 'demande_produit')
    df = pd.DataFrame(donnees)

    if df.empty:
        raise ValueError("Not enough data to train the model.")

    # Remove outliers if necessary
    q_low = df["prix_produit"].quantile(0.01)
    q_hi  = df["prix_produit"].quantile(0.99)
    df_filtered = df[(df["prix_produit"] < q_hi) & (df["prix_produit"] > q_low)]

    # Separate independent (X) and dependent (y) variables
    X = df_filtered[['offre_produit', 'demande_produit']]
    y = df_filtered['prix_produit']

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Create and train the linear regression model
    modele = LinearRegression()
    modele.fit(X_train, y_train)

    # Check the model score
    print(f"Model score: {modele.score(X_test, y_test)}")

    # Save the model and scaler
    modele_path = os.path.join(settings.BASE_DIR, 'marche', 'modele_prix.joblib')
    joblib.dump(modele, modele_path)

    scaler_path = os.path.join(settings.BASE_DIR, 'marche', 'scaler.joblib')
    joblib.dump(scaler, scaler_path)

    print("Model and scaler trained and saved successfully.")

@login_required
@user_passes_test(is_admin_or_superadmin)
def analyse_prix_ia2(request):
    modele_path = os.path.join(settings.BASE_DIR, 'marche', 'modele_prix.joblib')
    scaler_path = os.path.join(settings.BASE_DIR, 'marche', 'scaler.joblib')

    # Load the linear regression model
    if not os.path.exists(modele_path) or not os.path.exists(scaler_path):
        return render(request, 'marche/afficher_toutes_donnees.html', {
            'message': "The AI model or scaler has not yet been trained."
        })
    
    modele = joblib.load(modele_path)
    scaler = joblib.load(scaler_path)

    # Retrieve all market data
    donnees = DonneeMarche.objects.all()
    resultats = []

    for donnee in donnees:
        # Prepare data for prediction
        X_nouvelle = [[donnee.offre_produit, donnee.demande_produit]]

        # Make a prediction using the trained model
        prix_predit = modele.predict(scaler.transform(X_nouvelle))[0]  # Scale the new data
        prix_predit = round(prix_predit, 2)

        # Store results
        resultats.append({
            'produit': donnee.produit,
            'prix_predit': prix_predit,
            'nouvelle_demande': donnee.demande_produit,
            'nouvelle_offre': donnee.offre_produit
        })

    return render(request, 'marche/analysestoutedonne.html', {
        'resultats': resultats
    })
