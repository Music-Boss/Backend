from django.contrib import admin
from .models import Cancion, Curso, Lista, Usuario, Rockola
# Register your models here.

#admin.site.register(Curso)
admin.site.register(Usuario)
admin.site.register(Cancion)
admin.site.register(Lista)
admin.site.register(Rockola)