from django.shortcuts import render
from .models import Servicio


def lista_servicios(request):

    # Obtenemos todos los clientes de la base de datos
    servicios = Servicio.objects.all()

    #enviamos los datos al template
    return render(request, 'servicios/lista.html', {'servicios':servicios})
