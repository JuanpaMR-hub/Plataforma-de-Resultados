from configparser import ConfigParser
import json
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Alternativa, Item, Usuario, Pertenece, Colegio, Nivel, Letra, Actividadxreim, Reim, Actividad, AsignaReim, Graficoxactividad, ObjetivoAprendizaje, ItemAlt
from embed_report.services.pbiembedservice import PbiEmbedService

# Create your views here.


@login_required
def home_view(request):
    logged_user = request.user
    if(logged_user.username == 'admin'):
        logout(request)
        return redirect("../")

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
    nombre_curso = Nivel_elegido + " "+Letra_elegida

    #Incorporar Periodo
    periodo = ""
    mes = int(fecha[5:7])
    if(mes > 0 and mes < 7):
        periodo = fecha[0:4]+"01"
    else:
        periodo = fecha[0:4]+"02"

    Reims = AsignaReim.objects.filter(periodo_id= periodo,colegio_id = id_colegio, nivel_id = id_nivel, letra_id = id_letra)
    for i in Reims:
        nombre_reims.append(Reim.objects.get(id=i.reim_id))

    curso = {
        "nivel": id_nivel,
        "letra": id_letra,
        "fecha": fecha,
        "colegio": id_colegio,
    }
    


    context['nombre_curso'] = nombre_curso
    context['curso']=curso
    context['Reim'] = nombre_reims
    return render(request, "pages/home_reim.htm",context)


@login_required
def lobby_view(request,fecha,reim_id, id_colegio, id_nivel, id_letra):
    context = {}
    nombre_actividad = []
    actividades_con_preguntas = [40003,40010]
    reim = Reim.objects.get(id = reim_id)
    

    actividad = Actividadxreim.objects.filter(id_reim=reim_id)
    for i in actividad:
        nombre_actividad.append(Actividad.objects.get(id = i.id_actividad.id))
    

    curso = {
        "nivel": id_nivel,
        "letra": id_letra,
        "fecha": fecha,
        "colegio": id_colegio,
    }
    

    context['reim_escogido'] = reim
    context['curso']=curso
    context['actividades_permitidas'] = actividades_con_preguntas
    context['actividad'] = nombre_actividad
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
        
    actividad = Actividad.objects.get(id = actividad_id)
    context['object']=actividad
    context['alumnos'] = alumnos

    #Dando parametros a las funciones de JS
    curso =[
        {
            'fecha' : fecha,
            'colegio' : id_colegio,
            'nivel': id_nivel,
            'letra': id_letra
        }
    ]
    context['data'] = json.dumps(curso)

    #Cambiando el archivo config para acceder al reporte que se pide
    nombre_reporte = f"{actividad.nombre}"
    config = ConfigParser()
    config.read('./embed_report/configs/config.ini')
    
    WORKSPACE_ID = config.get('power_bi_app','WORKSPACE_ID')
    report_id=PbiEmbedService().get_report(WORKSPACE_ID,nombre_reporte)
    config.set('power_bi_app','REPORT_ID',report_id)
    with open(file='./embed_report/configs/config.ini',mode= 'w+') as f:
        config.write(f)

    return render(request, "Reim1/actividad.htm",context)

def get_embed_info(request):
    '''Returns report embed configuration'''
    try:
        config = ConfigParser()
        config.read('./embed_report/configs/config.ini')
        
        WORKSPACE_ID = config.get('power_bi_app','WORKSPACE_ID')
        REPORT_ID = config.get('power_bi_app','REPORT_ID')
        if(REPORT_ID != "Nada"):
            embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)
            return HttpResponse(embed_info)
        else:
            return HttpResponse("No hay un grafico disponible")
    except Exception as ex:
        print("hola")
        return json.dumps({'errorMsg': str(ex)}), 500
#------ De momento esta queda deshabilitada --------------
@login_required
def resultados_generales_view(request,fecha,reim_id, id_colegio, id_nivel, id_letra):
    context = {}
    try:
        grafico = Graficoxactividad.objects.get(id_actividad = reim_id).embedurl
    except:
        grafico = 0
    # grafico_a_traer = 'GraficaActividad'+str(actividad_id)
    # grafico = traer_reporte(grafico_a_traer)
    context['grafico'] = grafico
    
    return render(request, "Reim1/g_generales.htm",context)



#------ Inicio proceso "Creación de Preguntas y sus alternativas"--------
def crearPreguntas_view(request,fecha,reim_id, id_colegio, id_nivel, id_letra):
    context = {}
    oa = ObjetivoAprendizaje.objects.all()
    
    context['oa'] = oa
    context['nivel'] = id_nivel
    return render(request, "pages/crearPregunta.htm",context)

def crearAlternativas_view(request,fecha,reim_id, id_colegio, id_nivel, id_letra):
    context = {}
    pregunta = request.POST.get('txtpregunta')
    alternativas = 0
    oa = ObjetivoAprendizaje.objects.get(id = request.POST.get('oa'))
    

    #Pregunta
    ultimo = Item.objects.latest('iditem')
    p = Item(iditem = int(ultimo.iditem)+1,pregunta = pregunta, justificacion = request.POST.get('txtJustificacion'), reim_id = reim_id, objetivo_aprendizaje = oa)
    p.save()


    #Alternativa
    if(id_nivel > 4):
        alternativas = 3
    else:
        alternativas = 2
    #Creando lista para que el template pueda iterar dentro con la cantidad de alternativas
    lista = [*range(0,int(alternativas),1)]

    context['pregunta']= pregunta
    context['alternativas'] = lista
    context['letra'] = id_letra
    context['p']=p
    return render(request, "pages/crearAlternativas.htm",context)

#Esta view solo aparece si el usuario confirma la creación de la pregunta
def confirmacion_view(request,fecha,reim_id, id_colegio, id_nivel, id_letra,id_item):
    context = {}
    p = Item.objects.get(iditem = id_item)
    alternativas = request.POST.getlist('txtrespuesta')
    escorrecta = request.POST.getlist('correcta')
    url_a_redirigir = "../../"+id_letra

    #Guardar alternativas
    for i in alternativas:
        ultima_alternativa = Alternativa.objects.latest('idlaternativa')
        a = Alternativa(idlaternativa = int(ultima_alternativa.idlaternativa)+1, txt_alte = i)

        ultima_relacion_itemalt = ItemAlt.objects.latest('indice')
        r = ItemAlt(indice = int(ultima_relacion_itemalt.indice)+1,idlaternativa = a , escorrecto = escorrecta[alternativas.index(i)], item_iditem = p)

        a.save()
        r.save()



    context['pregunta'] = p.pregunta
    context['alternativas'] = alternativas
    context['url_a_redirigir'] = url_a_redirigir
    return render(request, "pages/confirmacion.htm",context)

#-------------- Fin proceso "Creación de Preguntas y sus alternativas"--------


#-------------------------------Alternativa--------------------
def alternativa_view(request):
    return render(request, "alternativa/resultados.htm")
#------------------------------Fin Alternativa-----------------

def ayuda_view(request,*args, **kwargs):
    return render(request, "pages/ayuda.htm",{})



# ----- Proceso de Login y Logout-----------------------------
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
    
# -----Fin proceso de Login y Logout-----------------------------