from django.shortcuts import render
from .models import Cliente
from rest_framework import viewsets
from .serializers import ClienteSerializer

# Vista HTML
def lista_clientes(request):

    # Obtenemos todos los clientes de la base de datos
    clientes = Cliente.objects.all()

    #enviamos los datos al template
    return render(request, 'clientes/lista.html', {'clientes': clientes})

# Vista API REST
class ClienteViewSet(viewsets.ModelViewSet):

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
