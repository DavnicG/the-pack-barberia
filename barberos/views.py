from django.shortcuts import render
from .models import Barbero
from rest_framework import viewsets
from .serializers import BarberoSerializer

# Vista HTML
def lista_barberos(request): 

    # Obtenemos todos los barberos de la base de datos
    barberos = Barbero.objects.all()

    # Enviamos los datos al template
    return render(request, 'barberos/lista.html', {'barberos': barberos})

# Vista API REST
class BarberoViewSet (viewsets.ModelViewSet):

    queryset = Barbero.objects.all()
    serializer_class = BarberoSerializer