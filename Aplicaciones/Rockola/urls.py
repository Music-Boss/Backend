from django.urls import path
from .import views 

urlpatterns = [
    path('', views.homepage),
    #path('registrarCurso/', views.registrarCurso),
    #path('edicionCurso/<codigo>',views.edicionCurso),
    #path('editarCurso/',views.editarCurso),
    #path('eliminarCurso/<codigo>', views.eliminarCurso),
    #Rutas rockola
    path('rockola/test',views.salaRockola),
    path('rockola/id/<codigo>',views.salaInicialRockola),
    path('rockola/id/<codigo>/<listaId>',views.salaPersonalizadaRockola),
    path('registrarCancionRockola/',views.registrarCancionRockola),
    path('eliminarCancionRockola/<idRockola>/<idCancion>',views.eliminarCancionRockola),
    #Url login y registro 24/09/21
    path('login/', views.autenticarUsuario),
    path('logout/', views.cerrarSesionUsuario),
    path('registro/',views.registrarUsuario),
    #Rutas usuario
    path('home/',views.userHome),
]