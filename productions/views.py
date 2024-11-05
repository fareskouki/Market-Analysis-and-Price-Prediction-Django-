from django.shortcuts import render, redirect, get_object_or_404
from .models import Production
from .forms import ProductionForm

# Lister les productions
def production_list(request):
    productions = Production.objects.all()
    return render(request, 'productions/production_list.html', {'productions': productions})

# Créer une nouvelle production
def production_create(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('production_list')
    else:
        form = ProductionForm()
    return render(request, 'productions/production_form.html', {'form': form})

# Mettre à jour une production
def production_update(request, pk):
    production = get_object_or_404(Production, pk=pk)
    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=production)
        if form.is_valid():
            form.save()
            return redirect('production_list')
    else:
        form = ProductionForm(instance=production)
    return render(request, 'productions/production_form.html', {'form': form})

# Supprimer une production
def production_delete(request, pk):
    production = get_object_or_404(Production, pk=pk)
    if request.method == 'POST':
        production.delete()
        return redirect('production_list')
    return render(request, 'productions/production_confirm_delete.html', {'production': production})
