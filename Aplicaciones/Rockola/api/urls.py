from django.urls.conf import include
from Aplicaciones.Rockola.api.views import (
    CancionViewSet,
    ListaViewSet,
    RockolaViewSet,
    UsuarioViewSet
)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'canciones', CancionViewSet)
router.register(r'listas', ListaViewSet)
router.register(r'rockolas',RockolaViewSet)

urlpatterns = [
    path('', include(router.urls))
]
