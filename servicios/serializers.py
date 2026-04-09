from rest_framework import serializers
from .models import Servicio

class ServicioSerializer(serializers.ModelSerializer):

    class Meta:

        model = Servicio
        fields = '__all__' # id, nombre, duracion_min, precio