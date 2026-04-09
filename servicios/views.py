from django.shortcuts import render
from .models import Servicio
from rest_framework import viewsets
from .serializers import ServicioSerializer

# Vista HTML
def lista_servicios(request):

    # Obtenemos todos los clientes de la base de datos
    servicios = Servicio.objects.all()

    #enviamos los datos al template
    return render(request, 'servicios/lista.html', {'servicios':servicios})

# Vista API REST
class ServicioViewSet (viewsets.ModelViewSet):

    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer