from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('registrarCurso/', views.registrarCurso),
    path('edicionCurso/<codigo>',views.edicionCurso),
    path('editarCurso/',views.editarCurso),
    path('eliminarCurso/<codigo>', views.eliminarCurso),
    #Rutas rockola
    path('rockola/test',views.salaRockola),
    path('rockola/id/<codigo>',views.salaInicialRockola),
    path('rockola/id/<codigo>/<listaId>',views.salaPersonalizadaRockola),
    path('registrarCancionRockola/',views.registrarCancionRockola),
    path('eliminarCancionRockola/<idRockola>/<idCancion>',views.eliminarCancionRockola)
]