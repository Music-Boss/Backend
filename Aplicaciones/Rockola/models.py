from datetime import datetime, date

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.forms import widgets

# Create your models here.

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Correo'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Contraseña'


class Amigo(models.Model):
    usuario = models.OneToOneField(User, primary_key=True ,related_name="usuario", on_delete=models.CASCADE)
    amigos = models.ManyToManyField(User, related_name="amigos", blank=True)
    #models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="amigo", blank=True, null=True)

    def __str__(self):
        texto = "{0}: Amigos"
        return texto.format(self.usuario)

"""
class Usuario(models.Model):
    username = models.CharField(primary_key=True,max_length=16)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    email = models.EmailField()
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=256)
    #blank=True indica que los siguientes atributos no son obligatorios dentro del modelo
    fechaNacimiento = models.DateField(blank=True,null=True)
    
    def __str__(self):
        texto = "{0} ({1} {2})"
        return texto.format(self.username, self.nombre, self.apellido)
"""

class Cancion(models.Model):
    idCancion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    fuente = models.CharField(max_length=256)
    esKaraoke = models.BooleanField()
    artista = models.CharField(max_length=60)
    #blank=True indica que los siguientes atributos no son obligatorios dentro del modelo
    album = models.CharField(max_length=128, blank=True)
    fechaPublicacion = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    letras = models.TextField(blank=True)
    def __str__(self):
        texto = "{0}: {1} - {2} - {3}"
        return texto.format(self.idCancion, self.artista, self.album, self.nombre)
    
class Lista(models.Model):
    idLista = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cover = models.CharField(max_length=256, blank=True)
    fechaCreacion = models.DateField(default= date.today)
    #Relacion uno a muchos con Usuario
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    #Relacion muchos a muchos con Cancion
    canciones = models.ManyToManyField(Cancion)

    def __str__(self):
        texto = "{0} - {1} - {2}"
        return texto.format(self.idLista, self.usuario, self.nombre)


class Rockola(models.Model):
    idRockola = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cover = models.CharField(max_length=256, blank=True)
    #Relacion uno a muchos con Usuario
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    #Relacion muchos a muchos con Lista
    listas = models.ManyToManyField(Lista)
    canciones = models.ManyToManyField(Cancion, through='Playlist', blank=True)

    def __str__(self):
        texto = "{0} - {1}: {2}"
        return texto.format(self.idRockola, self.usuario, self.nombre)

class PlayList(models.Model):
    idPlaylist = models.AutoField(primary_key=True)
    rockola = models.ForeignKey(Rockola, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    dateTimeAdded = models.DateTimeField(default=datetime.now)

    def __str__(self):
        texto = "({0}) {1} - {2}"
        return texto.format(self.dateTimeAdded, self.rockola, self.cancion)