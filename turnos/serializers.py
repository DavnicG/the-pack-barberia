from rest_framework import serializers
from .models import Turno

class TurnoSerializer(serializers.ModelSerializer):

    # En lugar de devolver el ID del barbero, devolvemos su nombre
    # source='barbero.nombre' le dice a DRF de dónde sacar el dato
    barbero_nombre = serializers.CharField(source='barbero.nombre',  read_only=True)

    # Igual para el servicio
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)

    # Formateamos fecha y hora para que la app los muestre directamente
    fecha = serializers.DateField(format='%d/%m/%Y')
    hora  = serializers.TimeField(format='%H:%M')

    class Meta:

        model = Turno
        
        # Devolvemos solo los campos que necesita la app móvil
        fields = [
            'id',
            'fecha',
            'hora',
            'estado',
            'metodo_pago',
            'barbero_nombre',
            'servicio_nombre',
        ]

