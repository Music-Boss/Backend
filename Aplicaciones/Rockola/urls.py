from django.urls import path
from .import views 

urlpatterns = [
    path('', views.home),
    path('registrarCurso/', views.registrarCurso),
    path('edicionCurso/<codigo>',views.edicionCurso),
    path('editarCurso/',views.editarCurso),
    path('eliminarCurso/<codigo>', views.eliminarCurso),
    #Url login y registro 24/09/21
    path('login/',views.vistalogin),
    path('registro/',views.registro),
    path('registrarUsuario/',views.registrarUsuario),
    path('ingresarUsuario/',views.ingresarUsuario),
    
    
]