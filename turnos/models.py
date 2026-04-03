from django.db import models

#Importamos los modelos relacionados
from clientes.models import Cliente
from barberos.models import Barbero
from servicios.models import Servicio

class Turno (models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')]
    
    METODOS_PAGO = [
        ('efectivo','EFECTIVO'),
        ('tarjeta','TARJETA'),
        ('transferencia','TRANSFERENCIA')
    ]

    fecha = models.DateField()

    hora = models.TimeField()

    estado = models.CharField(
        max_length=10,          # Máximo 10 caracteres (suficiente para 'estado')
        choices=ESTADOS,        # Solo permite los valores definidos arriba
        default= 'pendiente'    # Si no se especifica, se asigna 'Pendiente'
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Se guarda automático

    cliente = models.ForeignKey(
        Cliente,                    #Modelo al que apunta la llave foranea
        on_delete=models.RESTRICT   #No permite borrar si tiene turnos asociados
    )

    barbero = models.ForeignKey(
        Barbero,                    #Modelo al que apunta la llave foranea
        on_delete=models.RESTRICT   #No permite borrar si tiene turnos asociados
    )

    servicio = models.ForeignKey(
        Servicio,                    #Modelo al que apunta la llave foranea
        on_delete=models.RESTRICT   #No permite borrar si tiene turnos asociados
    )

    metodo_pago = models.CharField(
        max_length=15,
        choices=METODOS_PAGO,
        default='efectivo'
    )

    def __str__(self):
        return f"{self.cliente} - {self.fecha}"


