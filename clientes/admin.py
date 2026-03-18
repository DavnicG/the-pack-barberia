from django.contrib import admin

# Importamos el modelo de esta app
from .models import Cliente

# Registramos el modelo para que aparezca en el panel
admin.site.register(Cliente)
