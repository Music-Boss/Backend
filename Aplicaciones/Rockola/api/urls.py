from django.urls.conf import include
from Aplicaciones.Rockola.api.views import (
    CancionViewSet,
    ListaViewSet,
    RockolaViewSet,
    UsuarioViewSet,
    UserInfoViewSet,
    SolicitudViewSet,
    login,
    addRockolaCancion,
    removeRockolaCancion,
    usuarioAmigo,
    usuarioListaFavorita,
    usuarioRockolaFavorita,
    sendSolicitud,
    aceptarSolicitud,
)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'usuario/info',UserInfoViewSet)
router.register(r'solicitudes', SolicitudViewSet)
router.register(r'canciones', CancionViewSet)
router.register(r'listas', ListaViewSet)
router.register(r'rockolas',RockolaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login),
    path('rockola/<rockolaId>/canciones/add/<cancionId>/',addRockolaCancion),
    path('rockola/<rockolaId>/canciones/remove/<cancionId>/',removeRockolaCancion),
    path('usuario/<userId>/amigos/<amigoId>/',usuarioAmigo),
    path('usuario/<userId>/fav/listas/<listaId>/',usuarioListaFavorita),
    path('usuario/<userId>/fav/rockolas/<rockolaId>/',usuarioRockolaFavorita),
    path('usuario/<remitenteId>/solicitud/<destinatarioId>/',sendSolicitud),
    #path('usuario/<usuarioId>/lista/',crearLista),
    #path('usuario/<usuarioId>/rockola/',crearRockola),
    #path('usuario/<usuarioId>/add/',crearUsuario),
    path('usuario/<remitenteId>/solicitud/<destinatarioId>/aceptar/',aceptarSolicitud),
]
