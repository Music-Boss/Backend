from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers
from Aplicaciones.Rockola.models import Cancion, Lista, Rockola, PlayList
from .serializers import CancionSerializer, UsuarioSerializer, ListaSerializer, RockolaSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from django.contrib.auth.models import User

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class CancionViewSet(viewsets.ModelViewSet):
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer

class ListaViewSet(viewsets.ModelViewSet):
    queryset = Lista.objects.all()
    serializer_class = ListaSerializer

class RockolaViewSet(viewsets.ModelViewSet):
    queryset = Rockola.objects.all()
    serializer_class = RockolaSerializer