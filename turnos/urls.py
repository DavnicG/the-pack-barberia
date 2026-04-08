from django.urls import path
from . import views

urlpatterns = [
    # Con barbero preseleccionado: /turnos/crear/2/
    path('crear/<int:barbero_id>/', views.crear_turno, name='crear_turno'),
    # Sin barbero preseleccionado: /turnos/crear/
    path('crear/', views.crear_turno, name='crear_turno_general'),
    # Ruta para Mis Citas
    path('mis-citas/', views.mis_citas, name='mis_citas'),
]