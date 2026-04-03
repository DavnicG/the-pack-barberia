from django.shortcuts import render, redirect

from barberos.models import Barbero
from servicios.models import Servicio
from clientes.models import Cliente

from .forms import TurnoForm

def crear_turno(request, barbero_id=None):

# Traemos todos los barberos y servicios de la BD
    barberos = Barbero.objects.all()
    servicios = Servicio.objects.all()

# Si el usuario envió el formulario (botón Reservar)
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            # commit=False → no guarda aún en la BD, nos da el objeto para modificarlo
            if request.user.is_authenticated:
                # Si está logueado, buscamos o creamos su Cliente
                cliente, _ = Cliente.objects.get_or_create(

                    email= request.user.email,
                    defaults= {'nombre': request.user.username}
                )
            else:
                # Si es invitado, tomamos los datos del formulario
                cliente, _ = Cliente.objects.get_or_create(
                    email=request.POST.get('email'),
                    defaults={
                        'nombre': request.POST.get('nombre'),
                        'telefono': request.POST.get('telefono'),
                    }
                )
            turno.cliente = cliente
            turno.save()
            return redirect('lista_barberos')

    else:
        # Si viene con barbero_id, lo preseleccionamos
        initial = {}
        if barbero_id:

            initial['barbero'] = barbero_id
        
        form = TurnoForm(initial=initial)
    
    return render (request, 'turnos/crear.html', {
        'form': form,
        'barberos': barberos,
        'servicios': servicios,
        'barbero_id': barbero_id,
        })