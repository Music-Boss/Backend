from django.contrib import admin
from .models import Amigo, Cancion, Lista, PlayList, Rockola
# Register your models here.

admin.site.register(Amigo)
admin.site.register(Cancion)
admin.site.register(Lista)
admin.site.register(Rockola)
admin.site.register(PlayList)