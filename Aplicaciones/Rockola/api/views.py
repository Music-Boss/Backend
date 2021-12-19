import json
from rest_framework import viewsets, response, permissions
from rest_framework import serializers
from rest_framework.fields import REGEX_TYPE
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers

### API AUTH ###
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from Aplicaciones.Rockola.models import Cancion, Lista, Rockola, Amigo
from .serializers import CancionSerializer, UsuarioSerializer, ListaSerializer, RockolaSerializer, AmigoSerializer

### Custom permissions ###
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

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
            
        return False
            

class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class AmigoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Amigo.objects.all()
    serializer_class = AmigoSerializer

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
