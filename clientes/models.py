from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


# Validador que solo permite dígitos, espacios, + y guiones
# Ejemplo válido: +57 300 123 4567 o 3001234567
telefono_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{7,15}$',
    message='Ingresa un número de teléfono válido. Solo números, espacios, + y guiones.'
)


class Cliente(models.Model):

    # OneToOneField → un Usuario tiene exactamente un Cliente y viceversa
    # null=True, blank=True → permite que existan clientes sin cuenta (usuarios invitados)
    # on_delete=SET_NULL → si se borra el User, el Cliente queda pero sin usuario asociado
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete= models.SET_NULL,
        null=True,
        blank=True,
        related_name='cliente'      # permite acceder con: request.user.cliente
    )

    nombre= models.CharField(max_length=100)

    telefono=models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[telefono_validator]
    )

    email= models.EmailField(
        unique=True,
        blank=True,
        null=True 
    )

    fecha_registro=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
