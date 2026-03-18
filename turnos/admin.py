from django.contrib import admin

# Importamos el modelo de esta app
from .models import Turno

# Registramos el modelo para que aparezca en el panel
admin.site.register(Turno)
