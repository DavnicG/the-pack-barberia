from django.shortcuts import render, redirect
from django.contrib import messages

from barberos.models import Barbero
from servicios.models import Servicio
from clientes.models import Cliente
from .models import Turno
from .forms import TurnoForm 


def crear_turno(request, barbero_id=None):
    """
    Vista principal para crear un turno.
    Funciona para dos rutas:
      - /turnos/crear/         → sin barbero preseleccionado
      - /turnos/crear/<id>/    → con barbero preseleccionado
    """

    # Traemos todos los barberos y servicios de la BD para mostrar en el formulario
    barberos = Barbero.objects.all()
    servicios = Servicio.objects.all()

    # ─────────────────────────────────────────────────────────────
    # CASO 1: El usuario envió el formulario (botón Confirmar Reserva)
    # ─────────────────────────────────────────────────────────────
    if request.method == 'POST':

        form = TurnoForm(request.POST)
        
        if form.is_valid():

            # commit=False → crea el objeto Turno pero NO lo guarda aún en la BD
            # Necesitamos asignarle el cliente antes de guardar
            turno = form.save(commit=False)
            
            # ── Determinar el cliente ──────────────────────────────
            if request.user.is_authenticated:

                # Usuario logueado: buscamos su Cliente por email
                # Si no existe, lo creamos con su username
                cliente, _ = Cliente.objects.get_or_create(

                    email= request.user.email,
                    defaults= {'nombre': request.user.username}
                )
            else:

                # Usuario invitado: tomamos los datos del formulario
                # get_or_create evita duplicados si el email ya existe
                cliente, _ = Cliente.objects.get_or_create(
                    email=request.POST.get('email'),
                    defaults={
                        'nombre': request.POST.get('nombre'),
                        'telefono': request.POST.get('telefono'),
                    }
                )

            # ── Verificar que el horario no esté ocupado ───────────
            # Buscamos si ya existe un turno con el mismo barbero, fecha y hora
            turno_existente = Turno.objects.filter(

                barbero = turno.barbero,
                fecha = turno.fecha,
                hora = turno.hora,
                estado__in=['pendiente', 'confirmado'] # Solo bloqueamos activos
            ).exists()

            if turno_existente:
                # Si ya está ocupado, mostramos un aviso y no guardamos
                messages.error(
                request,
                'Ese horario ya está reservado. Por favor elige otra hora.'
                )
            else:
                # Todo está bien → asignamos cliente y guardamos
                turno.cliente = cliente
                turno.save()    

                # Redirigimos a la pagina de 'Mis citas'
                messages.success(request, '¡Tu cita fue reservada con éxito!')
                return redirect('mis_citas')
            
        # Si el formulario tiene errores, caemos aquí
        # Django renderiza de nuevo la página con los errores

    # ─────────────────────────────────────────────────────────────
    # CASO 2: El usuario abrió la página por primera vez (GET)
    # ─────────────────────────────────────────────────────────────
    else:
        # Si viene con barbero_id, lo ponemos como valor inicial del form
        initial = {}
        if barbero_id:

            initial['barbero'] = barbero_id
        
        form = TurnoForm(initial=initial)
    
    # Enviamos todo al template
    return render (request, 'turnos/crear.html', {
        'form': form,
        'barberos': barberos,
        'servicios': servicios,
        'barbero_id': barbero_id,
        })

def mis_citas(request):
    """
    Muestra los turnos del cliente logueado.
    Si no está autenticado, lo redirige al login o permite busqueda por correo.
    """
    turnos = []
    email_buscado = None

    # Si no inició sesión, no tiene citas que mostrar
    if  request.user.is_authenticated:

        # Usuario logueado: buscamos por su email automáticamente
        try:
            cliente = Cliente.objects.get(email=request.user.email)
            # Traemos sus turnos ordenados del más reciente al más antiguo
            turnos = Turno.objects.filter(
                cliente=cliente
            ).order_by('-fecha', '-hora')
        except Cliente.DoesNotExist:
            # Si aún no tiene perfil de cliente, lista vacía
            turnos = []

    elif request.method == 'POST':

        # Usuario invitado: busca por el email que ingresó
        email_buscado = request.POST.get('email_busqueda', '').strip()

        try:

            cliente = Cliente.objects.get(email = email_buscado)
            turnos = Turno.objects.filter(
                cliente = cliente
            ).order_by('-fecha', '-hora')
        
        except Cliente.DoesNotExist:

            # Email no encontrado en la BD
            messages.error(request, 'No encontramos citas con este correo.')

        
    return render(request, 'turnos/mis_citas.html', {
        'turnos': turnos,
        'email_buscado': email_buscado,
    })