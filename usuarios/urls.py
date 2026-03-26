# Importamos path para definir las rutas URL
from django.urls import path
# Importamos las vistas que acabamos de crear
from . import views

# urlpatterns es la lista que Django lee para saber qué vista
# llamar según la URL que visita el usuario
urlpatterns = [
    
    # /login/ → muestra el formulario de login o lo procesa
    path('login/', views.vista_login, name='login'),

    # /registro/ → muestra el formulario de registro o lo procesa
    path('registro/', views.vista_registro, name='registro'),

    # /logout/ → cierra la sesión y redirige al inicio
    path('logout/', views.vista_logout, name= 'logout'),
]
