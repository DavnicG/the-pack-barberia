from django.shortcuts import render, redirect

from .forms import TurnoForm

def crear_turno(request, barbero_id):

# Si el usuario envió el formulario (botón Reservar)
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_barberos')

    # Si el usuario solo está visitando la página
    else:
        form = TurnoForm(initial={'barbero': barbero_id})
    
    return render (request, 'turnos/crear.html', {'form': form})