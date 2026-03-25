from django.db import models


class Barbero(models.Model):

    nombre = models.CharField(max_length=100)  # Requerido por defecto

    telefono = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )

    especialidad = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    # Campo para la foto
    foto = models.ImageField(
        upload_to= 'barberos/', # se guarda en media/barberos/
        blank= True,
        null= True
    )

    def __str__(self):
        # Muestra el nombre del barbero como texto
        return self.nombre