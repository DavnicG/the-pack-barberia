# Importamos las herramientas de formularios de Django
from django import forms

# Importamos el modelo Turno
from .models import Turno

class TurnoForm (forms.ModelForm):

    class Meta:

        model = Turno
        fields = ['barbero', 'servicio', 'fecha', 'hora']