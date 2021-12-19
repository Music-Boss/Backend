import json
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm

from MusicBoss.settings import AUTH_PASSWORD_VALIDATORS
from .models import Rockola, Cancion, CustomUserForm
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

def autenticarUsuario(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            if request.POST.get('txtUsuario') is not None: #Si el txtUser no está vacío
                username = request.POST.get('txtUsuario')
                password = request.POST.get('txtContraseña')
            else: #Se asume que si no, llega una petición JSON en el body del request
                bodyRes = json.loads(request.body.decode("utf-8"))
                username = bodyRes['username']
                password = bodyRes['password']
            
            print(f"username: {username}, password: {password}, request body: {request.body} ")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                messages.info(request, "El nombre de usuario o la contraseña son incorrectos")
        return render(request,"registration/login.html")

def cerrarSesionUsuario(request):
    logout(request)
    return redirect('/')

def registrarUsuario(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        form = CustomUserForm()
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, "¡El usuario "+ username + " fue creado exitosamente!")
                return redirect('/login/')
    
        context = {'form' : form }
        return render(request,"registration/registro.html", context)

#Vistas Usuario

@login_required(login_url='/login/')
def userHome(request):
    return render(request, "usuario/home.html")

#Vista Principal

def homepage(request):
    return render(request, "home/homepage.html")