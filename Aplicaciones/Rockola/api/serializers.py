from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django_countries.serializers import CountryFieldMixin
from Aplicaciones.Rockola.models import Cancion, Lista, Rockola, UserInfo, Solicitud


class UsuarioSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        # These fields are only editable (not displayed) and have to be a part of 'fields' tuple
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
    
    #validate_password = make_password

class UserInfoSerializer(CountryFieldMixin, serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(UserInfoSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = UserInfo
        fields = '__all__'
        depth = 1

class SolicitudSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(SolicitudSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Solicitud
        fields = '__all__'
        depth = 1

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = '__all__'

class ListaSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(ListaSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    
    class Meta:
        model = Lista
        fields = '__all__'
        depth = 1

class RockolaSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(RockolaSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2
    
    class Meta:
        model = Rockola
        fields = '__all__'
        depth = 2