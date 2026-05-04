from django.urls import path
from . import views

urlpatterns = [
    # Con barbero preseleccionado: /turnos/crear/2/
    path('crear/<int:barbero_id>/', views.crear_turno, name='crear_turno'),
    # Sin barbero preseleccionado: /turnos/crear/
    path('crear/', views.crear_turno, name='crear_turno_general'),
    # Ruta para Mis Citas
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    #URL para el AJAX de horas ocupadas
    path('horas-ocupadas/', views.horas_ocupadas, name='horas_ocupadas'),
    # URL para cancelar
    # <int:turno_id> → Django captura el número del ID y lo pasa a la vista
    # Ejemplo: /turnos/cancelar/5/ → cancela el turno con ID 5
    path('cancelar/<int:turno_id>', views.cancelar_turno, name='cancelar_turno'),
]