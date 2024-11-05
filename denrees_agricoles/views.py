from django.shortcuts import render, redirect
from .models import DenreesAgricoles
from .forms import DenreesAgricolesForm
import pandas as pd
from django.http import JsonResponse, HttpResponse  # Add HttpResponse here
from django.views.decorators.http import require_POST
import io
import numpy as np
import matplotlib
matplotlib.use('SVG')  # Utiliser le backend SVG
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def create_denree(request):
    if request.method == 'POST':
        form = DenreesAgricolesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_denrees')
    else:
        form = DenreesAgricolesForm()
    return render(request, 'create_denree.html', {'form': form})

def list_denrees(request):
    denrees = DenreesAgricoles.objects.all()
    return render(request, 'list_denrees.html', {'denrees': denrees})

def update_denree(request, id):
    denree = DenreesAgricoles.objects.get(id=id)
    if request.method == 'POST':
        form = DenreesAgricolesForm(request.POST, instance=denree)
        if form.is_valid():
            form.save()
            return redirect('list_denrees')
    else:
        form = DenreesAgricolesForm(instance=denree)
    return render(request, 'update_denree.html', {'form': form})

def delete_denree(request, id):
    denree = DenreesAgricoles.objects.get(id=id)
    if request.method == 'POST':
        denree.delete()
        return redirect('list_denrees')
    return render(request, 'delete_denree.html', {'denree': denree})

def import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return render(request, 'import_csv.html', {'error': 'Le fichier n\'est pas au format CSV.'})
        
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            DenreesAgricoles.objects.create(
                domain_code=row['Domain Code'],
                domain=row['Domain'],
                area_code=row['Area Code (M49)'],
                area=row['Area'],
                element_code=row['Element Code'],
                element=row['Element'],
                item_code=row['Item Code (CPC)'],
                item=row['Item'],
                year_code=row['Year Code'],
                
                year=row['Year'],
                months_code=row['Months Code'],
                months=row['Months'],
                unit=row['Unit'],
                value=row['Value'],
                flag=row['Flag'],
                flag_description=row['Flag Description'],
            )
        
        return redirect('list_denrees')
    
    return render(request, 'import_csv.html')

def import_csv_chart(request):
    if request.method == "POST":
        # Charger le fichier CSV envoyé par l'utilisateur
        csv_file = request.FILES['csv_file']
        df = pd.read_csv(csv_file)

        # Assurez-vous que les colonnes nécessaires existent dans le CSV
        if 'Year' not in df.columns or 'Value' not in df.columns:
            return JsonResponse({"error": "Les colonnes 'Year' et 'Value' sont manquantes dans le fichier CSV"}, status=400)

        # Extraire les données pour le graphique
        data = {
            "years": df['Year'].tolist(),  # Les années pour l'axe X
            "values": df['Value'].tolist()  # Les valeurs pour l'axe Y
        }

        return JsonResponse(data)  # Retourner les données sous forme de JSON
    return JsonResponse({"error": "Méthode non permise"}, status=405)

# Vue pour rendre le template HTML avec le graphique
def chart_view(request):
    return render(request, 'chart_template.html')
    if request.method == "POST":
        # Lire le fichier CSV
        df = pd.read_csv(request.FILES['csv_file'])

        # Vérifier les colonnes spécifiques et structurer les données pour le graphique
        # Supposons qu'on veut un graphique basé sur les colonnes 'Year' et 'Value'
        data = {
            "years": df['Year'].tolist(),
            "values": df['Value'].tolist()
        }

        return JsonResponse(data)  # Envoie les données en JSON au frontend
    return JsonResponse({"error": "Méthode non permise"}, status=400)
def forecast_prices(request):
    # Récupérer les données de "Sugar"
    DenreesAgricoles_data = DenreesAgricoles.objects.filter(item='Sugar beet').order_by('year')
    years = [DenreesAgricoles.year for DenreesAgricoles in DenreesAgricoles_data]
    values = [DenreesAgricoles.value for DenreesAgricoles in DenreesAgricoles_data]

    # Vérifier si des données existent
    if not years or not values or len(years) != len(values):
        return render(request, 'DenreesAgricoles/chart.html', {'error': 'Aucune donnée disponible ou les dimensions ne correspondent pas.'})

    # Convertir les données en format numpy
    x = np.array(years).reshape(-1, 1)
    y = np.array(values)

    # Appliquer la régression linéaire
    model = LinearRegression()
    model.fit(x, y)

    # Faire des prévisions pour l'année 2030 uniquement
    future_year = np.array([2030]).reshape(-1, 1)
    prediction = model.predict(future_year)

    # Créer un graphique
    plt.figure(figsize=(10, 5))
    plt.scatter(years, values, color='blue', label='Données historiques')
    plt.plot(years, model.predict(x), color='red', label='Régression linéaire')
    plt.scatter(future_year, prediction, color='green', label='Prévision pour 2030')
    plt.xlabel('Année')
    plt.ylabel('Prix (USD/tonne)')
    plt.title('Prévision des prix du sugar')
    plt.legend()
    plt.grid()

    # Enregistrer dans un objet BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='svg')
    plt.close()
    buf.seek(0)

    # Retourner la réponse HTTP avec le graphique SVG
    return HttpResponse(buf.getvalue(), content_type='image/svg+xml')
