from django.db import models

class Cliente(models.Model):

    nombre= models.CharField(max_length=100)

    telefono=models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email= models.EmailField(
        unique=True,
        blank=True,
        null=True 
    )

    fecha_registro=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
