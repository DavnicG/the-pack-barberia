from django.shortcuts import render
from .models import Cliente

def lista_clientes(request):

    # Obtenemos todos los clientes de la base de datos
    clientes = Cliente.objects.all()

    #enviamos los datos al template
    return render(request, 'clientes/lista.html', {'clientes': clientes})
