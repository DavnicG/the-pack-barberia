from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ── Importamos todos los ViewSets ──────────────────────
from barberos.views import BarberoViewSet
from clientes.views import ClienteViewSet
from servicios.views import ServicioViewSet
from turnos.views import TurnoViewSet

# ── Registramos los endpoints en el router ─────────────
router = DefaultRouter()
router.register(r'barberos',  BarberoViewSet)
router.register(r'clientes',  ClienteViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'turnos',    TurnoViewSet)

urlpatterns = [
    # ── URLs existentes ──────────────────
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('barberos/', include('barberos.urls')),
    path('clientes/', include('clientes.urls')),
    path('servicios/', include('servicios.urls')),
    path('turnos/', include('turnos.urls')),
    path('', include('usuarios.urls')),

    # ── API REST ───────────────────────────────
    path('api/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)