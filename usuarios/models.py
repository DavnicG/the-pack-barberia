# Importamos AbstractUser, el modelo de usuario base de Django
from django.contrib.auth.models import AbstractUser
# Importamos models para poder usar los tipos de campos
from django.db import models

class Usuario(AbstractUser):
    
    # Definimos las opciones válidas para el campo rol
    ROLES = [
        ('admin', 'Administrador'),  #('valor en BD', 'Texto visible')
        ('barbero', 'Barbero')
    ]

    # Campo rol: texto corto, usa las opciones de arriba, por defecto 'barbero'
    rol = models.CharField(
        max_length=10,      # Máximo 10 caracteres (suficiente para 'barbero')
        choices=ROLES,      # Solo permite los valores definidos arriba
        default='barbero'   # Si no se especifica, se asigna 'barbero'
    ) 

    def __str__(self):
        # Cuando Django muestre este objeto como texto, mostrará el nombre de usuario
        return self.username
