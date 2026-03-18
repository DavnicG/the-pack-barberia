from django.shortcuts import render
from barberos.models import Barbero

def index(request):
    """Página principal del sitio"""
    barberos = Barbero.objects.all()

    return render(request, 'index.html', {'barberos': barberos})