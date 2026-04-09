from rest_framework import serializers
from .models import Barbero

class BarberoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Barbero
        fields = '__all__'  # id, nombre, telefono, especialidad, foto