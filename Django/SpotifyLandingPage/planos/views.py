from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from planos.models import Planos

def lista_planos(request):
    lista_de_planos = Planos.objects.all().order_by('id')
    print(lista_de_planos)
    return render(request, 'premium.html', { 'planos': lista_de_planos })