from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Ulearnet, Usuario, Pertenece, Colegio, Nivel, Letra, Actividadxreim
# Create your views here.

def home_view(request):
    logged_user = request.user
    userID = str(logged_user.ulearnet.id_ulearnet)
    user = Usuario.objects.get(id=userID)
    pertenece = Pertenece.objects.all()
    id_colegios = []
    colegios = {}

    #En la siguiente operación se rellena un diccionario en donde se almacena los datos de colegios y sus cursos. Para evitar repeticiones de estos, se llena y compara una lista de los colegios que ya se han guardado
    for p in pertenece:
        print(p.usuario_id, "== ",userID)
        if(p.usuario_id == userID):
            #Si el colegio se repite
            if p.colegio_id in id_colegios:

                #Ingresando el nombre de cada uno de los componentes para utilizarlos en el template
                lista_anterior = colegios.get(Colegio.objects.get(idcolegio = p.colegio_id).nombre_colegio)
                lista_agregar = [Nivel.objects.get(idnivel = p.nivel_id).nombre_nivel , Letra.objects.get(idletra = p.letra_id).letra_id]

                colegios[Colegio.objects.get(idcolegio=p.colegio_id).nombre_colegio] = lista_anterior + [lista_agregar]
            else:

                #Ingresando los datos en la lista Id colegios
                id_colegios.append(p.colegio_id)


                #Ingresando los datos de los nombres de los componentes
                key = Colegio.objects.get(idcolegio=p.colegio_id).nombre_colegio
                value_nivel = Nivel.objects.get(idnivel = p.nivel_id).nombre_nivel
                value_letra =  Letra.objects.get(idletra = p.letra_id).letra_id

                colegios[key] = [[value_nivel, value_letra]]
    context = { 
        'usuario': user,
        'colegio' : colegios,
     }
    return render(request, 'pages/home.htm', context)






def home_reim_view(request,*args, **kwargs):
    context = {}
    system = request.POST.get('system')
    context['system'] = system
    return render(request, "pages/home_reim.htm",context)

def lobby_view(request,*args, **kwargs):
    #Super bien con las ids pero el usuario necesita saber los nombres de estos reims y actividades
    context = {}
    nombre_actividad = []

    reim_escogido = request.POST.get('botonreim',None)
    #reim = Reim.objects.get(id = reim_escogido)
    context['reim_escogido'] = reim_escogido

    actividad = Actividadxreim.objects.filter(id_reim=reim_escogido)
    #for i in actividad:
       # nombre_actividad.append(Actividad.objects.get(id = i.id_actividad))

    context['actividad'] = actividad



    return render(request, "Reim1/reim_lobby.htm",context)

def actividad_view(request,mi_id):
    #obj = Actividad.objects.get(id_actividad = mi_id)
    context = {
       # "object":obj
    }
    return render(request, "Reim1/actividad.htm",context)

def ayuda_view(request,*args, **kwargs):
    return render(request, "pages/ayuda.htm",{})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            #Log in user
            user = form.get_user()
            login(request, user)
            return redirect("/home")
        else:
            #Buscar Usuario en BD Ulearnet
            user_name = request.POST.get("username")
            user_pass = request.POST.get("password")
            try:
                usuario = Usuario.objects.get(usuario = user_name)
                if(usuario != None):
                    if(usuario.contrasena == user_pass):
                    #Crear usuario en la BD de Django
                        crearUsuario(usuario.usuario, usuario.contrasena, usuario.id)
                        formulario = AuthenticationForm(data= request.POST)
                        user = formulario.get_user()
                        login(request, user)
                        return redirect('/home')
            except:
                print("Hubo un error, no se encontro el usuario en la BD de Ulearnet")
               
    else:
        form = AuthenticationForm()
    return render(request, 'Registration/login.html', {'form':form})
    # En vez de form podria pasar el id del usuario, de esa manera en la pagina poder pedir los colegios y cursos del docente

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('../')



def crearUsuario(username,password, user_id):
    user = User.objects.create_user(username,"",password)
    u = Ulearnet.objects.create(id_ulearnet = user_id, user_id = user.pk)
    user.save()
    u.save()