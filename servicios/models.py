from django.db import models


class Servicio(models.Model):

    nombre = models.CharField(max_length=100)  # Requerido

    duracion_min = models.IntegerField(
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=8,      # Total de dígitos: ej. 999999.99
        decimal_places=2,  # Dígitos después del punto: ej. .99
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre
