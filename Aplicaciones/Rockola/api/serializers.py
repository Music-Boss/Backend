from rest_framework import serializers
from django.contrib.auth.models import User
from Aplicaciones.Rockola.models import Cancion, Lista, Rockola, PlayList

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        write_only_fields = ['password']

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = '__all__'

class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = '__all__'

class RockolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rockola
        fields = '__all__'