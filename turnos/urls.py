from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:barbero_id>/', views.crear_turno, name='crear_turno'),
]