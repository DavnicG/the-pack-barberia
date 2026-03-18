from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Admin base de Django para usuarios

# Importamos el modelo de esta app
from .models import Usuario

class UsuarioAdmin(UserAdmin):

    # Agregamos 'rol' a los campos que se muestran en el listado
    list_display = ('username', 'email', 'rol', 'is_staff')

    # Agregamos 'rol' al formulario de edición de usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en la barbería', {'fields': ('rol',)}),
    )

# Registramos el modelo para que aparezca en el panel
admin.site.register(Usuario, UsuarioAdmin)
