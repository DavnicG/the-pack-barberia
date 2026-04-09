from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'email', 'fecha_registro']
        # Excluimos 'usuario' por seguridad