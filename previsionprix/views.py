from django.shortcuts import render, get_object_or_404, redirect
from .models import PrévisionPrix
from .forms import PrévisionPrixForm
#vieww
def prevision_list(request):
    previsions = PrévisionPrix.objects.all()
    
    return render(request, 'previsionprix/prevision_list.html', {'previsions': previsions})

def prevision_detail(request, id):
    prevision = get_object_or_404(PrévisionPrix, id=id)
    return render(request, 'previsionprix/prevision_detail.html', {'prevision': prevision})

def prevision_create(request):
    if request.method == 'POST':
        form = PrévisionPrixForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('previsionprix/prevision_list')
    else:
        form = PrévisionPrixForm()
    return render(request, 'previsionprix/prevision_form.html', {'form': form})

def prevision_update(request, id):
    prevision = get_object_or_404(PrévisionPrix, id=id)
    if request.method == 'POST':
        form = PrévisionPrixForm(request.POST, instance=prevision)
        if form.is_valid():
            form.save()
            return redirect('previsionprix/prevision_list')
    else:
        form = PrévisionPrixForm(instance=prevision)
    return render(request, 'previsionprix/prevision_form.html', {'form': form})

def prevision_delete(request, id):
    prevision = get_object_or_404(PrévisionPrix, id=id)
    if request.method == 'POST':
        prevision.delete()
        return redirect('prevision_list')
    return render(request, 'previsionprix/prevision_confirm_delete.html', {'prevision': prevision})
