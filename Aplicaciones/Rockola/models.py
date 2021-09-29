from django.db import models

# Create your models here.

class Curso(models.Model):
    codigo = models.CharField(primary_key=True,max_length=6) 
    nombre = models.CharField(max_length=50)
    creditos = models.PositiveSmallIntegerField()

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre, self.creditos)

class Usuario(models.Model):
    username = models.CharField(primary_key=True,max_length=16)
    email = models.EmailField()
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=256)
    #blank=True indica que los siguientes atributos no son obligatorios dentro del modelo
    fechaNacimiento = models.DateField(blank=True,null=True)
    
    def __str__(self):
        texto = "{0} ({1} {2})"
        return texto.format(self.username, self.nombre, self.apellido)


class Cancion(models.Model):
    idCancion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    fuente = models.CharField(max_length=256)
    esKaraoke = models.BooleanField()
    #blank=True indica que los siguientes atributos no son obligatorios dentro del modelo
    artista = models.CharField(max_length=60, blank=True)
    fechaPublicacion = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True)
    duracion = models.IntegerField(blank=True, null=True)
    letras = models.TextField(blank=True)
    
    def __str__(self):
        texto = "{0} - {1}"
        return texto.format(self.idCancion, self.nombre)
    
class Lista(models.Model):
    idLista = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaCreacion = models.DateField()
    #Relacion uno a muchos con Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #Relacion muchos a muchos con Cancion
    canciones = models.ManyToManyField(Cancion)

    def __str__(self):
        texto = "{0} - {1} - {2}"
        return texto.format(self.idLista, self.usuario, self.nombre)


class Rockola(models.Model):
    idRockola = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    #Relacion uno a muchos con Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #Relacion muchos a muchos con Lista
    listas = models.ManyToManyField(Lista)

    def __str__(self):
        texto = "{0} - {1}"
        return texto.format(self.idRockola, self.nombre)