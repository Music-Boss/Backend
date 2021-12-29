from django.contrib import admin
from .models import UserInfo, Cancion, Lista, PlayList, Rockola, Solicitud
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(Solicitud)
admin.site.register(Cancion)
admin.site.register(Lista)
admin.site.register(Rockola)
admin.site.register(PlayList)