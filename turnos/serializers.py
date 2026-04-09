from rest_framework import serializers
from .models import Turno

class TurnoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Turno
        fields = '__all__'  # id, fecha, hora, estado, cliente, barbero, servicio
