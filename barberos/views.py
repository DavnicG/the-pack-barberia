from django.shortcuts import render
from .models import Barbero

def lista_barberos(request): 

    # Obtenemos todos los barberos de la base de datos
    barberos = Barbero.objects.all()

    # Enviamos los datos al template
    return render(request, 'barberos/lista.html', {'barberos': barberos})