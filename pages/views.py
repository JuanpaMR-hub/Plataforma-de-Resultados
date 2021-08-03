from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Usuario, Pertenece, Colegio, Nivel, Letra, Actividadxreim, Reim, Actividad, AsignaReim
# Create your views here.


@login_required
def home_view(request):
    logged_user = request.user

    #Buscar otra opciones
    usuario = Usuario.objects.get(username=logged_user.username)

    pertenece = Pertenece.objects.filter(usuario_id = usuario.id)

    #En la siguiente operación se rellena un diccionario en donde se almacena los datos de colegios y sus cursos. Para evitar repeticiones de estos, se llena y compara una lista de los colegios que ya se han guardado
    cursos = []
    colegios = {}
    
    
    for p in pertenece:
        cursos.append(0)

        value_colegio = Colegio.objects.get(id=p.colegio_id)
        value_nivel = Nivel.objects.get(id = p.nivel_id)
        value_letra =  Letra.objects.get(id = p.letra_id)
        value_fecha = str(p.fecha)[0:-6]

        index = len(cursos)-1
        cursos[index] = {}
        cursos[index]["colegio"] = [value_colegio.nombre,value_colegio.id]
        cursos[index]["nivel"] = [value_nivel.nombre,value_nivel.id]
        cursos[index]["letra"] =[value_letra.nombre ,value_letra.id]
        cursos[index]["fecha"] = str(value_fecha)

        aux = {index : cursos[index]}
        if value_colegio.nombre in colegios:
            colegios[value_colegio.nombre].update(aux)
        else:
            colegios[value_colegio.nombre] = aux                
    context = { 
        'usuario': usuario,
        'colegios' : colegios,
     }
    return render(request, 'pages/home.htm', context)





@login_required
def home_reim_view(request,fecha,usuario_id, id_colegio, id_nivel, id_letra):
    context = {}
    nombre_reims = []
    Curso_elegido = Pertenece.objects.get(fecha = fecha,usuario_id= usuario_id , colegio_id = id_colegio, nivel_id = id_nivel, letra_id = id_letra)

    Nivel_elegido = Nivel.objects.get(id = Curso_elegido.nivel_id).nombre
    Letra_elegida = Letra.objects.get(id = Curso_elegido.letra_id).nombre
    periodo = ""

    #Incorporar Periodo
    mes = int(fecha[5:7])
    if(mes > 0 and mes < 7):
        periodo = fecha[0:4]+"01"
    else:
        periodo = fecha[0:4]+"02"

    Reims = AsignaReim.objects.filter(periodo_id= periodo,colegio_id = id_colegio, nivel_id = id_nivel, letra_id = id_letra)
    print(Reims)
    print(fecha)
    print(periodo)

    for i in Reims:
        print("REIM: ",i.reim_id)
        nombre_reims.append(Reim.objects.get(id=i.reim_id))

    curso = {
        "nivel": id_nivel,
        "letra": id_letra,
        "fecha": fecha,
        "colegio": id_colegio,
    }
    context['curso']=curso


    nombre_curso = Nivel_elegido + " "+Letra_elegida
    context['nombre_curso'] = nombre_curso
    context['curso']=curso
    context['Reim'] = nombre_reims
    return render(request, "pages/home_reim.htm",context)



@login_required
def lobby_view(request,fecha,reim_id, id_colegio, id_nivel, id_letra):
    #Super bien con las ids pero el usuario necesita saber los nombres de estos reims y actividades
    context = {}
    nombre_actividad = []

    reim = Reim.objects.get(id = reim_id)
    context['reim_escogido'] = reim

    actividad = Actividadxreim.objects.filter(id_reim=reim_id)
    for i in actividad:
        nombre_actividad.append(Actividad.objects.get(id = i.id_actividad.id))
    context['actividad'] = nombre_actividad

    curso = {
        "nivel": id_nivel,
        "letra": id_letra,
        "fecha": fecha,
        "colegio": id_colegio,
    }
    context['curso']=curso

    return render(request, "Reim1/reim_lobby.htm",context)

@login_required
def actividad_view(request,fecha,actividad_id, id_colegio, id_nivel, id_letra):
    context = {}
    alumnos = []

    #Encontrar los alumnos que están en esta actividad -> reimxperiodo
    año = fecha[0:4]

    p = Pertenece.objects.filter(fecha__startswith = año, colegio_id = id_colegio, nivel_id = id_nivel, letra_id = id_letra)

    for alumno_pertenece in p:
        alumno = Usuario.objects.get(id = alumno_pertenece.usuario_id)
        alumnos.append(alumno)
        

    obj = Actividad.objects.get(id = actividad_id)
    context['object']=obj
    context['alumnos'] = alumnos
    return render(request, "Reim1/actividad.htm",context)


def ayuda_view(request,*args, **kwargs):
    return render(request, "pages/ayuda.htm",{})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            #Log in user
            user = form.get_user()
            if(user.username != "admin"):
                login(request, user)
                return redirect("../")
        else:
            #Buscar Usuario en BD Ulearnet
            user_name = request.POST.get("username")
            user_pass = request.POST.get("password")
            try:
                usuario = Usuario.objects.get(username = user_name)
                if(usuario != None):
                    if(usuario.tipo_usuario_id != 3):
                        if(usuario.password == user_pass):
                            #Crear usuario en la BD de Django
                            crearUsuario(usuario.username, usuario.password, usuario.id)
                        
                            return redirect('../')
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
    user.save()
    