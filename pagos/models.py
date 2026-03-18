from django.db import models

#Importamos los modelos relacionados
from turnos.models import Turno

class Pago (models.Model):

    METODO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    monto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    metodo = models.CharField(
        max_length=15,
        choices=METODO,
        default='efectivo'
    )

    fecha = models.DateTimeField(auto_now_add=True)

    turno = models.ForeignKey(
        Turno,                    #Modelo al que apunta la llave foranea
        on_delete=models.CASCADE  # Si se borra el turno, se borra el pago
    )
    
    def __str__(self):
        return f"{self.metodo} - {self.monto}"