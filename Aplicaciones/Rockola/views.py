from MusicBoss.settings import AUTH_PASSWORD_VALIDATORS
from django.shortcuts import redirect, render
from .models import Curso, Rockola, Cancion, Usuario
from django.contrib import messages



# Create your views here.

def home(request):
    cursosList = Curso.objects.all()
    messages.success(request,"¡Cursos Listados!")
    return render(request, "gestionCursos.html", {"cursos": cursosList})

def registrarCurso(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    creditos = request.POST['numCreditos']

    curso=Curso.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
    messages.success(request,"¡Curso Registrado!")
    return redirect('/')

def edicionCurso(request, codigo):
    curso = Curso.objects.get(codigo=codigo)
    return render(request,"edicionCurso.html",{"curso": curso})

def editarCurso(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    creditos = request.POST['numCreditos']

    curso = Curso.objects.get(codigo=codigo)
    curso.nombre = nombre
    curso.creditos = creditos
    curso.save()
    messages.success(request,"¡Curso Actualizado!")
    return redirect('/')

def eliminarCurso(request, codigo):
    curso = Curso.objects.get(codigo=codigo)
    curso.delete()
    messages.success(request,"¡Curso Eliminado!")
    return redirect('/')

#Sala Rockola

def salaRockola(request):
    return render(request, "sala-rockola.html")

def salaInicialRockola(request, codigo):
    rockola = Rockola.objects.get(idRockola=codigo)
    listas = rockola.listas.all()
    canciones = rockola.canciones.all()
    #print(listas.values()[0]["idLista"])
    context = []
    for lista in listas:
        print(lista.nombre)
        item = {
            "id": lista.idLista,
            "canciones" : lista.canciones.all().values()
        }
        if(lista.idLista == listas.values()[0]["idLista"]):
            context.append(item)
            break
    print(type(context[0]["id"]))
    return render(request, "sala-rockola.html",{"rockola": rockola, "listaId": context[0]["id"], "listas": listas, "canciones": canciones, "context": context})

def salaPersonalizadaRockola(request, codigo, listaId):
    rockola = Rockola.objects.get(idRockola=codigo)
    listas = rockola.listas.all()
    canciones = rockola.canciones.all()
    listaIdInt =  int(listaId)
    context = []
    for lista in listas:
        print(lista.nombre)
        item = {
            "id": lista.idLista,
            "canciones" : lista.canciones.all().values()
        }
        if(lista.idLista == listaIdInt):
            context.append(item)
            break
    return render(request, "sala-rockola.html",{"rockola": rockola, "listaId": listaIdInt, "listas": listas, "canciones": canciones, "context": context})

def registrarCancionRockola(request):
    idCancion = request.POST['numCancion']
    idRockola = request.POST['numRockola']

    cancion = Cancion.objects.get(idCancion = idCancion)
    rockola = Rockola.objects.get(idRockola = idRockola)

    rockola.canciones.add(cancion)
    #print(cancion) 
    #print(rockola)
    return redirect('/rockola/id/'+idRockola)

def eliminarCancionRockola(request, idRockola, idCancion):
    cancion = Cancion.objects.get(idCancion = idCancion)
    rockola = Rockola.objects.get(idRockola = idRockola)

    rockola.canciones.remove(cancion)
    return redirect('/rockola/id/'+idRockola)

#Funciones para login
def vistalogin (request):
    return render(request, "registration/login.html")

def registro(request):
    return render(request, "registration/registro.html")

def registrarUsuario(request):
    nombreUsuario =request.POST['txtUsuario']
    email = request.POST['txtCorreo']
    nombre = request.POST['txtNombre']
    apellido = request.POST['txtApellido']
    contraseña = request.POST['txtContraseña']
    #fechaNacimiento = request.POST['txtDate']

    usuario=Usuario.objects.create(username=nombreUsuario,email=email,
    nombre=nombre,apellido=apellido,contraseña=contraseña)

    return redirect('/')

def ingresarUsuario(request):
    nombreUsuario =request.POST['txtUsuario']
    contraseña = request.POST['txtContraseña']

    usuario=Usuario.objects.create(username=nombreUsuario,contraseña=contraseña)
    return redirect ('/')

    #curso=Curso.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
    #messages.success(request,"¡Curso Registrado!")
    #return redirect('/')

