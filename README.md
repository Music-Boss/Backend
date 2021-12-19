# MusicBoss

Aplicación para la programación y reproducción sincronizada de música via streaming

### Crear proyecto nuevo:

django-admin startproject Universidad

### Crear una aplicación dentro de un proyecto:

(generalmente dentro de una carpeta conteniendo las aplicaciones)
djangoadmin startapp Academico

### Hacer la migración de la Base de Datos:

python manage.py migrate

### Migrar los nuevos modelos dentro de la Base de Datos:

python manage.py makemigrations

### Deshacer las migraciones hasta una migración específica

python manage.py migrate Rockola 0006_alter_cancion_artista

### Crear un superusuario para administrar el proyecto:

python manage.py createsuperuser

### Correr el Servidor

python manage.py runserver

### Guardar datos para usarlos como datos iniciales al reiniciar la db

python manage.py dumpdata

python manage.py loaddata <nombre_archivo>

### Repositorios

origin: Repositorio de GitLab
org: Repositorio de la origanización Music-Boss de GitHub
heroku: Despliegue en heroku

## Administración Heroku

### Ver logs

heroku logs --tail

### Ver la base de datos (Postgres)

heroku pg:psql

### Borrar la base de datos del server

heroku pg:reset DATABASE_URL

### Conectarse al dyno (servidor) para ejecutar comandos en bash

heroku run bash

Nota: Sólo puede haber una conexión al bash






