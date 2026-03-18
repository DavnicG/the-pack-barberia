from django.urls import path
from . import views

urlpatterns = [
    # URL: /barberos/  →  llama a la vista lista_barberos
    path('', views.lista_barberos, name='lista_barberos')
]
