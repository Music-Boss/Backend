from curses.ascii import US
import json
from rest_framework import viewsets, response, permissions
from rest_framework import serializers
from rest_framework.fields import REGEX_TYPE
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers

### API AUTH ###
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from Aplicaciones.Rockola.models import Cancion, Lista, Rockola, Solicitud, UserInfo
from .serializers import (
    CancionSerializer, 
    UsuarioSerializer, 
    ListaSerializer, 
    RockolaSerializer, 
    UserInfoSerializer, 
    SolicitudSerializer
    )

### Custom permissions ###
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(f" request.user: {dir(request)}")
        print(f" request.data: {request.data}")
        bodyRes = request.data
        has_atrib = "remitente" in bodyRes
        print(f" hasatrib: {has_atrib}")
        if request.method == 'POST':
            if "remitente" in request.data: #Si se intenta crear una nueva solicitud
                return False
            else:
                return True
        elif request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        has_atrib = hasattr(obj,"usuario")
        print(f" request.user: {request.user}, obj: {obj}, hasattr: { has_atrib}")
        
        if hasattr(obj, "id"):
            # Si el objeto es un user 
            if obj == request.user:
                return True
            # Si el objeto es una lista, amigo o una rockola (tiene el atributo "usuario")
        
        if hasattr(obj,"usuario"):
            # Si la referencia al usuario en el objeto no es nula y el usuario actual es el dueño del objeto
            if obj.usuario != None and obj.usuario == request.user:
                return True
        
        #Si el objeto es una solicitud, puede ser editada tanto por el remitente como por el destinatario
        if hasattr(obj, "remitente"):
            if obj.remitente != None and obj.remitente == request.user:
                return True
            elif obj.destinatario != None and obj.destinatario == request.user:
                return True

        return False


class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class UserInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

class CancionViewSet(viewsets.ModelViewSet):
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer

class ListaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Lista.objects.all()
    serializer_class = ListaSerializer

class RockolaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Rockola.objects.all()
    serializer_class = RockolaSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    if request.POST.get('username') is not None: #Si el txtUser no está vacío
        username = request.POST.get('username')
        password = request.POST.get('password')
    else: #Se asume que si no, llega una petición JSON en el body del request
        bodyRes = request.data
        username = bodyRes['username']
        password = bodyRes['password']

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Usuario inválido")

    pwd_valid = check_password(password, user.password)

    if not pwd_valid:
        return Response("Contraseña incorrecta")

    token, created = Token.objects.get_or_create(user=user)

    print(token.key)
    return Response(token.key)

@api_view(['POST'])
@permission_classes([AllowAny])
def addRockolaCancion(request, rockolaId, cancionId):

    try:
        rockola = Rockola.objects.get(idRockola=rockolaId)
    except Rockola.DoesNotExist:
        return Response("La rockola con el id dado no existe")
    
    try:
        cancion = Cancion.objects.get(idCancion=cancionId)
    except Cancion.DoesNotExist:
        return Response("La canción con el id dado no existe")

    try:
        rockola.canciones.add(cancion)
        return Response("La canción ha sido agregada correctamente")
    except:
        return Response("Error agregando la canción")

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeRockolaCancion(request, rockolaId, cancionId):

    headersRes = request.headers
    authToken = headersRes["Authorization"][6:] #Token del user autenticado
    try:
        user = Token.objects.get(key=authToken).user
    except User.DoesNotExist:
        return Response("El token del usuario no es válido")

    try:
        rockola = Rockola.objects.get(idRockola=rockolaId)
    except Rockola.DoesNotExist:
        return Response("La rockola con el id dado no existe")
    
    try:
        cancion = Cancion.objects.get(idCancion=cancionId)
    except Cancion.DoesNotExist:
        return Response("La canción con el id dado no existe")

    if rockola.usuario is not None:
        if rockola.usuario == user:
            try:
                rockola.canciones.remove(cancion)
                return Response("La canción ha sido quitada correctamente")
            except:
                return Response("Error agregando la canción")
        else:
            return Response("No está autorizado para editar esta rockola",status=401)
    else:
        return Response("Esta rockola no es editable por API",status=403)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def usuarioAmigo(request, userId, amigoId):

    headersRes = request.headers
    authToken = headersRes["Authorization"][6:] #Token del user autenticado
    try:
        user = Token.objects.get(key=authToken).user
    except User.DoesNotExist:
        return Response("El token del usuario no es válido")

    try:
        usuario = User.objects.get(id = userId)
    except User.DoesNotExist:
        return Response("El id del usuario no es válido")
    
    try:
        amigo = User.objects.get(id = amigoId)
    except User.DoesNotExist:
        return Response("El id del amigo no es válido")

    try:
        userinfo = UserInfo.objects.get(usuario=userId)
    except UserInfo.DoesNotExist:
        return Response("El usuario ingresado no existe")
    
    try:
        amigoinfo = UserInfo.objects.get(usuario=amigoId)
    except UserInfo.DoesNotExist:
        return Response("El amigo ingresado no existe")

    if user == usuario:
        userinfo.amigos.remove(amigoId)
        amigoinfo.amigos.remove(userId)
        return Response("El amigo ha sido quitado correctamente")
    else:
        return Response("No está autorizado para editar este campo",status=401)
    

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def usuarioListaFavorita(request, userId, listaId):

    headersRes = request.headers
    authToken = headersRes["Authorization"][6:] #Token del user autenticado
    try:
        user = Token.objects.get(key=authToken).user
    except User.DoesNotExist:
        return Response("El token del usuario no es válido")

    try:
        usuario = User.objects.get(id = userId)
    except User.DoesNotExist:
        return Response("El id del usuario no es válido")
    
    try:
        lista = Lista.objects.get(idLista = listaId)
    except Lista.DoesNotExist:
        return Response("El id de la lista no es válido")

    try:
        userinfo = UserInfo.objects.get(usuario=userId)
    except UserInfo.DoesNotExist:
        return Response("El usuario ingresado no existe")
    
    if request.method == 'POST':
        if user == usuario:
            userinfo.fav_listas.add(listaId)
            return Response("La lista ha sido agregada correctamente")
        else:
            return Response("No está autorizado para editar este campo",status=401)
    elif request.method == 'DELETE':
        if user == usuario:
            userinfo.fav_listas.remove(listaId)
            return Response("La lista ha sido quitada correctamente")
        else:
            return Response("No está autorizado para editar este campo",status=401)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def usuarioRockolaFavorita(request, userId, rockolaId):

    headersRes = request.headers
    authToken = headersRes["Authorization"][6:] #Token del user autenticado
    try:
        user = Token.objects.get(key=authToken).user
    except User.DoesNotExist:
        return Response("El token del usuario no es válido")

    try:
        usuario = User.objects.get(id = userId)
    except User.DoesNotExist:
        return Response("El id del usuario no es válido")
    
    try:
        rockola = Rockola.objects.get(idRockola = rockolaId)
    except Rockola.DoesNotExist:
        return Response("El id de la rockola no es válido")

    try:
        userinfo = UserInfo.objects.get(usuario=userId)
    except UserInfo.DoesNotExist:
        return Response("El usuario ingresado no existe")
    
    if request.method == 'POST':
        if user == usuario:
            userinfo.fav_rockolas.add(rockolaId)
            return Response("La rockola ha sido agregada correctamente")
        else:
            return Response("No está autorizado para editar este campo",status=401)
    elif request.method == 'DELETE':
        if user == usuario:
            userinfo.fav_rockolas.remove(rockolaId)
            return Response("La rockola ha sido quitada correctamente")
        else:
            return Response("No está autorizado para editar este campo",status=401)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def sendSolicitud(request, remitenteId, destinatarioId):
    
    headersRes = request.headers
    authToken = headersRes["Authorization"][6:] #Token del user autenticado
    try:
        user = Token.objects.get(key=authToken).user
    except User.DoesNotExist:
        return Response("El token del usuario no es válido")
    
    try:
        remitente = User.objects.get(id = remitenteId)
    except User.DoesNotExist:
        return Response("El id del remitente no es válido")
    
    try:
        destinatario = User.objects.get(id = destinatarioId)
    except User.DoesNotExist:
        return Response("El id del destinatario no es válido")
    
    if request.method == 'POST':
        try:
            if user == remitente:
                solicitud = Solicitud(remitente=remitente,destinatario=destinatario)
                solicitud.save()
                return Response("La solicitud ha sido enviada correctamente")
            else:
                return Response("No está autorizado para crear este objeto",status=401)
        
        except:
            return Response("Ha ocurrido un error en la creación de la solicitud (¿La solicitud ya existe?)")
    elif request.method == 'DELETE':
        try:
            print(f"user: {user}, remitente: {remitente}, destinatario: {destinatario}")
            if user == remitente or user == destinatario:
                solicitud = Solicitud.objects.get(remitente=remitente,destinatario=destinatario)
                solicitud.delete()
                return Response("La solicitud ha sido eliminada correctamente")
            else:
                return Response("No está autorizado para eliminar este objeto",status=401)
        
        except:
            return Response("Ha ocurrido un error en la eliminación de la solicitud (¿La solicitud existe?)")

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def aceptarSolicitud(request, remitenteId, destinatarioId):
    
    headersRes = request.headers
    authToken = headersRes["Authorization"][6:] #Token del user autenticado
    try:
        user = Token.objects.get(key=authToken).user
    except User.DoesNotExist:
        return Response("El token del usuario no es válido")
    
    try:
        remitente = User.objects.get(id = remitenteId)
    except User.DoesNotExist:
        return Response("El id del remitente no es válido")
    
    try:
        destinatario = User.objects.get(id = destinatarioId)
    except User.DoesNotExist:
        return Response("El id del destinatario no es válido")
    
    try:
        userinfo_remitente = UserInfo.objects.get(usuario=remitenteId)
    except UserInfo.DoesNotExist:
        return Response("El remitente ingresado no existe")
    
    try:
        userinfo_destinatario = UserInfo.objects.get(usuario=destinatarioId)
    except UserInfo.DoesNotExist:
        return Response("El destinatario ingresado no existe")

    try:
        solicitud = Solicitud.objects.get(remitente=remitente,destinatario=destinatario)
    except Solicitud.DoesNotExist:
        return Response("No se puede aceptar una solicitud que no existe")

    try:
        if user == destinatario:
            userinfo_remitente.amigos.add(destinatarioId)
            userinfo_destinatario.amigos.add(remitenteId)
            solicitud.delete()
            try:
                solicitud2 = Solicitud.objects.get(remitente=destinatario,destinatario=remitente)
                solicitud2.delete()
            except Solicitud.DoesNotExist:
                pass
            
            return Response("La solicitud ha sido aceptada, !ahora ambos son amigos!")
        else:
            return Response("No está autorizado para aceptar esta solicitud",status=401)
    except:
        return Response("Ha ocurrido un error aceptando la solicitud")