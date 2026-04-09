# Importamos las herramientas necesarias
from django.shortcuts import render, redirect
# render    → construye el HTML y lo manda al navegador
# redirect  → manda al usuario a otra URL
from django.contrib.auth import authenticate, login, logout
# authenticate → verifica si el usuario y contraseña son correctos
# login        → inicia la sesión (guarda al usuario en la cookie)
# logout       → cierra la sesión
from django.contrib import messages
# messages → sistema de Django para mostrar mensajes temporales
# (errores, éxitos) que desaparecen después de mostrarse
from .models import Usuario
from clientes.models import Cliente

# ===== VISTA DE LOGIN =====

def vista_login(request):

    # Si el usuario YA está logueado, no tiene sentido que vea el login
    # Lo mandamos directo al inicio
    if request.user.is_authenticated:
        return redirect('index')
    
    # request.method dice cómo llegó el usuario a esta página:
    # GET  → simplemente visitó la URL (mostrar el formulario)
    # POST → envió el formulario (procesar los datos)

    if request.method == 'POST':

        # request.POST es un diccionario con los datos del formulario
        # las claves ('username', 'password') deben coincidir con los
        # atributos name="" del HTML
        username = request.POST['username'].lower()
        password = request.POST['password']

        # authenticate verifica en la BD si el usuario y contraseña son correctos
        # Si son correctos → devuelve el objeto usuario
        # Si son incorrectos → devuelve None
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:

            # El usuario y contraseña son correctos
            login(request, usuario)     # inicia la sesión oficialmente
            return redirect('index')    # manda al inicio
        
        else:

            # Usuario o contraseña incorrectos
            # messages.error guarda un mensaje de error para mostrar en el template
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # Si es GET (o si hubo error), mostramos el formulario de login
    return render(request, 'usuarios/login.html')


# ===== VISTA DE REGISTRO =====
def vista_registro(request):

    # Si ya está logueado, mandarlo al inicio
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':

        # Obtenemos los datos del formulario de registro
        username= request.POST['username'].lower()
        password1= request.POST['password1']
        password2= request.POST['password2']
        email= request.POST['email']

        # Verificamos que el nombre de usuario no esté ya tomado
        # .filter() busca en la BD, .exists() devuelve True/False

        if Usuario.objects.filter(username = username).exists():

            messages.error(request, 'Ese nombre de usuario ya existe')
        else:

            if password1 != password2:

                messages.error(request, 'Las contraseñas no coinciden')

            else:
                # create_user es un método especial que hashea (encripta) la contraseña
                
                usuario = Usuario.objects.create_user(

                    username=username,
                    password=password1,
                    email=email,
                    rol='cliente'   # todo usuario que se registre es cliente por defecto
                )

                # ── NUEVO: crear el Cliente vinculado al usuario ──────
                # Importa Cliente al inicio del archivo (ver abajo)
                # Esto garantiza que cada usuario registrado tenga su
                # perfil de Cliente listo para asociar turnos
                Cliente.objects.create(
                    usuario=usuario,        # ← vinculamos el User al Cliente
                    nombre=username,        # nombre inicial = username
                    email=email             # mismo email del registro
                )

                login(request, usuario)     # lo logueamos automáticamente al registrarse
                return redirect('index')    # manda al inicio
        
    # Si es GET mostramos el formulario de registro
    return render(request, 'usuarios/registro.html')

# ===== VISTA DE LOGOUT =====    
def vista_logout(request):

    logout(request)             # cierra la sesión, borra la cookie
    return redirect('index')    # manda al inicio sin sesión