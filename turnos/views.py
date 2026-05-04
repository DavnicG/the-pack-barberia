from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import TurnoSerializer

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
                
                    # Primero intentamos obtener el cliente por la relación directa usuario→cliente
                    try:
                        cliente = request.user.cliente

                    except Cliente.DoesNotExist:
                        # No tiene cliente vinculado aún — puede ser un usuario antiguo
                        # Intentamos encontrarlo por email antes de crear uno nuevo
                        cliente, created = Cliente.objects.get_or_create(
                            email=request.user.email,
                            defaults={
                                'nombre': request.user.username,
                            }
                        )
                        # Si lo encontramos por email, lo vinculamos al usuario para el futuro
                        if not created or cliente.usuario is None:
                            cliente.usuario = request.user
                            cliente.save()

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
            cliente = request.user.cliente
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

def horas_ocupadas(request):

    """
    Vista AJAX que devuelve las horas ya reservadas de un barbero en una fecha.
    El JS del formulario la consulta cada vez que cambia barbero o fecha.

    Recibe por GET:
        barbero_id → ID del barbero seleccionado
        fecha      → fecha en formato YYYY-MM-DD

    Devuelve JSON:
        { "ocupadas": ["09:00", "10:30", ...] }
    """

    barbero_id = request.GET.get('barbero_id')
    fecha = request.GET.get('fecha')

    # Si faltan parámetros, devolvemos lista vacía
    if not barbero_id or not fecha:
        return JsonResponse({'ocupadas': []})
    
    # Buscamos los turnos activos (pendiente o confirmado) de ese barbero en esa fecha
    turnos = Turno.objects.filter(
        barbero_id = barbero_id,
        fecha = fecha,
        estado__in = ['pendiente', 'confirmado']
    ).values_list('hora', flat=True)    #→ devuelve solo la columna hora como lista plana
                                        # Ejemplo: [datetime.time(9, 0), datetime.time(10, 30)]
    
    # Convertimos los objetos time a strings "HH:MM" para enviarlos como JSON
    ocupadas = [h.strftime('%H:%M') for h in turnos]

    return JsonResponse ({'ocupadas': ocupadas})

def cancelar_turno(request, turno_id):
    """
    Vista para cancelar un turno existente.
    
    Solo permite cancelar si:
    - El turno pertenece al cliente logueado (seguridad)
    - El estado es 'pendiente' o 'confirmado' (no cancelar lo ya completado)
    
    turno_id → viene de la URL, identifica qué turno cancelar
    """

    # Buscamos el turno en la BD por su ID
    # Si no existe, Django devuelve error 404 automáticamente
    turno = get_object_or_404(Turno, id=turno_id)

    # ── Seguridad: verificar que el turno le pertenece al usuario logueado ──
    # Evita que alguien cancele el turno de otro cliente poniendo otro ID en la URL
    if request.user.is_authenticated:
        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist :
            messages.error(request, 'No tienes permiso para cancelar este turno.')
            return redirect('mis_citas')
    
    # ── Verificar que el turno se puede cancelar ──
    # No tiene sentido cancelar algo ya completado o ya cancelado
    if turno.estado in ['pendiente', 'confirmado']:

        turno.estado = 'cancelado'  # Cambiamos el estado
        turno.save()                # Guardamos en la BD
        messages.success(request, 'Tu cita fue cancelada correctamente')
    else:
        messages.error(request, 'Este turno no se puede cancelar')
    
    return redirect('mis_citas')

# ── API REST ─────

class TurnoViewSet (viewsets.ModelViewSet):

    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer