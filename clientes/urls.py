from django.urls import path
from . import views

urlpatterns = [
    # URL: /clientes/  →  llama a la vista lista_clientes
    path('',views.lista_clientes, name='lista_clientes')
]
