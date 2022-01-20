from configparser import ConfigParser
import json
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone, dateformat
from .models import ActividadOa, Alternativa, AlumnoRespuestaActividad, Elemento, Item, Usuario, Pertenece, Colegio, Nivel, Letra, Actividadxreim, Reim, Actividad, AsignaReim, Graficoxactividad, ObjetivoAprendizaje, ItemAlt, DibujoReim, Aprueba, EvaluacionPropuesta
from embed_report.services.pbiembedservice import PbiEmbedService
from datetime import datetime

import base64
from django.db.models import Count
# Create your views here.


@login_required
def home_view(request):
    logged_user = request.user
    print(logged_user.username)
    if(logged_user.username == 'admin'):
        logout(request)
        return redirect("../")

    usuario = Usuario.objects.get(username=logged_user.username)
    pertenece = Pertenece.objects.filter(usuario_id = usuario.id)

    #En la siguiente operación se rellena un diccionario en donde se almacena los datos de colegios y sus cursos. Para evitar repeticiones de estos, se llena y compara una lista de los colegios que ya se han guardado
    cursos = []
    colegios = {}
    iniciales = {}
    
    
    for p in pertenece:
        cursos.append(0)

        value_colegio = Colegio.objects.get(id=p.colegio_id)
        value_nivel = Nivel.objects.get(id = p.nivel_id)
        value_letra =  Letra.objects.get(id = p.letra_id)
        value_fecha = str(p.fecha)[0:-6]
        print(str(value_fecha))
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
            inicialesColegio = [ s[0] for s in value_colegio.nombre.split() ]
            stringIniciales = ''.join(inicialesColegio)
            iniciales[value_colegio.nombre] = stringIniciales



    context = { 
        'usuario': usuario,
        'colegios' : colegios,
        'iniciales': iniciales
     }
    print("Estos son los colegios del usuario: ",len(colegios))
    if(len(colegios) == 1):
        return render(request, 'pages/home-cursos.htm',context)
    return render(request, 'pages/home.htm', context)
        
def guardar_curso(request):
    colegio = request.GET['colegio']
    nivel = request.GET['nivel']
    letra = request.GET['letra']
    fecha = request.GET['fecha']

    request.session['colegio'] = colegio
    request.session['nivel'] = nivel
    request.session['letra'] = letra
    request.session['fecha'] = fecha


    curso = {
        'colegio' : colegio,
        'nivel' : nivel,
        'letra' : letra,
        'fecha' : fecha,
    }

    return JsonResponse(curso,safe = False)

@login_required
def home_reim_view(request):
    context = {}
    nombre_reims = []
    usuario = Usuario.objects.get(username = request.user.username)
    curso = {
        "nivel": request.session['nivel'],
        "letra": request.session['letra'],
        "fecha": request.session['fecha'],
        "colegio": request.session['colegio'],
    }
    

    Curso_elegido = Pertenece.objects.get(fecha = curso['fecha'],usuario_id= usuario.id , colegio_id = curso['colegio'], nivel_id = curso['nivel'], letra_id = curso['letra'])
    Nivel_elegido = Nivel.objects.get(id = Curso_elegido.nivel_id).nombre
    Letra_elegida = Letra.objects.get(id = Curso_elegido.letra_id).nombre
    nombre_curso = Nivel_elegido + " "+Letra_elegida

    #Incorporar Periodo
    periodo = ""
    mes = int(curso['fecha'][5:7])
    if(mes > 0 and mes < 7):
        periodo = curso['fecha'][0:4]+"01"
    else:
        periodo = curso['fecha'][0:4]+"02"

    Reims = AsignaReim.objects.filter(periodo_id= periodo,colegio_id = curso['colegio'], nivel_id = curso['nivel'], letra_id = curso['letra'])
    for i in Reims:
        nombre_reims.append(Reim.objects.get(id=i.reim_id))

    


    context['nombre_curso'] = nombre_curso
    context['curso']= json.dumps(curso)
    context['Reim'] = nombre_reims
    context['usuario'] = usuario
    return render(request, "pages/home_reim.htm",context)

def home_reim_ajax(request):
    data = {}
    actividades = {}

    reimSeleccionado = request.GET['reim']
    reim = Reim.objects.get(nombre = reimSeleccionado)
    obj_actividadesxreim = Actividadxreim.objects.filter(id_reim = reim.id)
    for a in obj_actividadesxreim:
        actividades[a.id_actividad.nombre] = a.id_actividad.id



    data[reimSeleccionado] = actividades
    curso = request.GET['curso']
    data['curso'] = curso
    data['id_reim'] = reim.id
    return JsonResponse({'data':data},safe = False)

#-------------------------------Resultados--------------------
#Tengo que pasar el reim_id por formulario
def alternativa_view(request,reim_id):
    context = {}
    nombre_reim = Reim.objects.get(id=reim_id).nombre

    fecha = request.session['fecha']
    id_colegio = request.session['colegio']
    id_nivel = request.session['nivel']
    id_letra = request.session['letra']

    #Datos del curso
    curso = {
        'fecha':fecha,
        'colegio':id_colegio,
        'nivel':id_nivel,
        'letra':id_letra
    }

    #Actividades
    auxiliar = Actividadxreim.objects.filter(id_reim = reim_id)
    actividades = []
    for i in auxiliar:
        actividades.append(Actividad.objects.get(id = i.id_actividad.id))

    #Usuario
    usuario = Usuario.objects.get(username = request.user.username)


    #Agregando todo al contexto
    context['nombre_reim'] = nombre_reim
    context['actividades'] = actividades
    context['jsoncurso'] = json.dumps(curso)
    context['curso'] = curso
    context['usuario'] = usuario
    return render(request, "alternativa/resultados.htm", context)

def contenido_view(request):
    data = {}

    #Actividad
    nombre_actividad = request.GET['actividad']
    id_actividad = request.GET['id_actividad']
    #OA
    aux = ActividadOa.objects.filter(id_actividad = id_actividad)
    if aux:
        for i in aux:
            data[i.id_oa.nombre] = i.id_oa.descripcion

    #Ingreso de datos
    data[id_actividad] = nombre_actividad
    return JsonResponse(data,safe = False)

def get_embed_info(request):
    '''Returns report embed configuration'''

    try:
        config = ConfigParser()
        config.read('./embed_report/configs/config.ini')

        nombre_actividad = request.GET['nombre_actividad']
        id_actividad = request.GET['id_actividad']
        nombre_reporte = "("+str(id_actividad)+")"+nombre_actividad

        #OJO AQUI, es para la funcionalidad de Apoderado
        print(Usuario.objects.get(username = request.user.username).tipo_usuario_id)
        if (Usuario.objects.get(username = request.user.username).tipo_usuario_id == 8):
            print("ES UN APODERADO")
            nombre_reporte += "-Apoderado"

        print(nombre_reporte)
        
        WORKSPACE_ID = config.get('power_bi_app','WORKSPACE_ID')
        REPORT_ID = PbiEmbedService().get_report(WORKSPACE_ID,nombre_reporte)
        if(REPORT_ID != "Nada"):
            embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)
            return HttpResponse(embed_info)
        else:
            return HttpResponse("No hay un grafico disponible")
    except Exception as ex:
        print("hola")
        return json.dumps({'errorMsg': str(ex)}), 500
#------------------------------Fin Resultados-----------------

#------ Inicio proceso "Creación de Preguntas y sus alternativas"--------
def crearPreguntas_view(request):
    context = {}
    nivel = request.sesion['nivel']
    oa = ObjetivoAprendizaje.objects.all()
    
    context['oa'] = oa
    context['nivel'] = nivel
    return render(request, "pages/crearPregunta.htm",context)

def crearAlternativas_view(request,reim_id):
    context = {}
    pregunta = request.POST.get('txtpregunta')

    id_nivel = request.session['nivel']
    id_letra = request.session['letra']

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


#--------------INICIO Funcion Revisar Dibujos---------------------
#Tengo que hacer que el id de la actividad pase por formulario
def revisar_dibujo_view(request,actividad_id):
    context = {}
    alumnos = []

    usuario = Usuario.objects.get(username = request.user.username)
    fecha = request.session['fecha']
    id_colegio = request.session['colegio']
    id_nivel = request.session['nivel']
    id_letra = request.session['letra']
    #-------------Traer Alumnos-----------------
    año = fecha[0:4]
    p = Pertenece.objects.filter(fecha__startswith = año, colegio_id = id_colegio, nivel_id = id_nivel, letra_id = id_letra)

    for alumno_pertenece in p:
        alumno = Usuario.objects.get(id = alumno_pertenece.usuario_id)
        if (alumno.tipo_usuario_id == 3):
            alumnos.append(alumno)
    #--------------------------------------------------------------------
    actividad = Actividad.objects.get(id = actividad_id)

    #-----------------------Curso----------
    curso = {
        'fecha':fecha,
        'colegio':id_colegio,
        'nivel':id_nivel,
        'letra':id_letra
    }

    context['alumnos'] = alumnos
    context['actividad'] = actividad
    context['curso'] = curso
    context['usuario'] = usuario
    return render(request, 'revisionDibujo/revision_dibujo.htm',context)


def traer_dibujos(request):
    alumno = request.GET['id_alumno']
    actividad = request.GET['id_actividad']
    dibujos_alumno = {}
    #------ Traer Dibujos ----------------
    dibujos_obj = DibujoReim.objects.filter(actividad_id = actividad).filter(usuario_id = alumno)
    for dibujo in dibujos_obj:
        revisado = Aprueba.objects.filter(idimagen = dibujo.id_dibujo_reim).exists()
        if not revisado:
            dibujos_alumno[dibujo.id_dibujo_reim] = base64.b64encode(dibujo.imagen).decode()
            
    #-------------------------------------
    return JsonResponse({'dibujos':dibujos_alumno},safe = False)

def respuesta_docente(request):
    data = {
    'idUsuario' : request.GET['idUsuario'],
    'idDibujo' :request.GET['idDibujo'],
    'fechaAprueba' : timezone.localtime(timezone.now()),
    'Justificacion' : request.GET['justificacion'],
    'esAprobado' : request.GET['aprueba']
    }
    
    aux = Aprueba(idusuario = Usuario.objects.get(id=data['idUsuario']),idimagen = data['idDibujo'], fecha_aprueba = data['fechaAprueba'], justificacion = data['Justificacion'], esaprobado = data['esAprobado'])
    aux.save()
    return JsonResponse({'data':data},safe = False) 
#---------------FIN Funcion Revisar Dibujos-----------------------


#----------------Inicio Funcion Evaluacion Propuesta-------------
def evaluacionPropuesta_view(request):
    context = {}
    alumnos_curso = {}
    alumnos_a_filtrar={}


    docente = Usuario.objects.get(username = request.user.username)
    fecha = request.session['fecha']
    id_colegio = request.session['colegio']
    id_nivel = request.session['nivel']
    id_letra = request.session['letra']

    
    #ALUMNOS DEL CURSO
    año = fecha[0:4]
    p = Pertenece.objects.filter(fecha__startswith = año, colegio_id = id_colegio, nivel_id = id_nivel, letra_id = id_letra)

    for alumno_pertenece in p:
        alumno = Usuario.objects.get(id = alumno_pertenece.usuario_id)
        if (alumno.tipo_usuario_id == 3):
            alumnos_curso[alumno.nombres] = alumno.id

    #RESPUESTAS DEL ALUMNO
    datos_alumnos = {}
    conteo = 1
    instancias = AlumnoRespuestaActividad.objects.filter(id_elemento = 203106).filter(correcta = 1)
    for nombre,id in alumnos_curso.items():
        respuestas_alumno = instancias.filter(id_user = id)
        comparativa_evaluacion = EvaluacionPropuesta.objects.filter(id_usuario = id).filter(id_docente = docente.id)
        if respuestas_alumno:
            for i in respuestas_alumno:
                if not comparativa_evaluacion.filter(fecha_creacion = i.datetime_touch.strftime("%Y-%m-%d %H:%M:%S")):
                    datos_alumnos[conteo] = [nombre,i,id]
                    conteo += 1
                    if(id in alumnos_a_filtrar.values()):
                        print("Este id ya existe")
                    else:
                        alumnos_a_filtrar[nombre] = id

    context['docente'] = docente
    context['alumnos'] = datos_alumnos
    context['alumnos_a_filtrar'] = alumnos_a_filtrar
    return render(request, 'funciones/evaluacion_propuesta/evaluacion_propuesta.htm',context)

def guardarCalificacion(request):
    respuesta = "Si"

    #Obtener datos de la instancia(id alumno, fecha creacion, id docente, fecha evaluacion, evaluacion, propuesta )
    elemento = Elemento.objects.get(id = 203106)
    id_alumno = Usuario.objects.get(id = request.GET['idAlumno'])
    print(request.GET['fechaCreacion'])
    print(type(request.GET['fechaCreacion']))
    fecha_creacion = datetime.strptime(request.GET['fechaCreacion'],"%Y-%m-%d %H:%M:%S")

    print(type(fecha_creacion))

    id_docente = Usuario.objects.get(username = request.user.username)
    fecha_evaluacion = str(dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
    evaluacion = request.GET['evaluacion']
    propuesta = request.GET['propuesta']

    #Guardar los datos en la tabla evaluacion propuesta
    todos = EvaluacionPropuesta.objects.all()
    for i in todos:
        print(i.fecha_creacion)
    aux = EvaluacionPropuesta(id_elemento = elemento, id_usuario = id_alumno, fecha_creacion = fecha_creacion, id_docente= id_docente, fecha_evaluacion = fecha_evaluacion, evaluacion = evaluacion, propuesta = propuesta )
    try:
        aux.save()
    except Exception as e: # work on python 3.x
        print(str(e))
        respuesta = "No"

    return JsonResponse(respuesta,safe = False)

def traer_datos(request):
    datos = {}
    conteo = 1

    #Traer alumno seleccionado con sus datos (id)
    alumno = Usuario.objects.get(id = request.GET['id_alumno'])
    #Encontrar instancias del alumno (que no estén en evaluacion_propuesta pero si en alumno_respuesta_actividad)
    instancias = AlumnoRespuestaActividad.objects.filter(id_user = alumno.id , id_elemento = 203106, correcta = 1 )
    comparativa = EvaluacionPropuesta.objects.filter(id_usuario = alumno.id, id_docente =  Usuario.objects.get(username = request.user.username).id)
    for i in instancias:
        if not comparativa.filter(fecha_creacion = i.datetime_touch.strftime("%Y-%m-%d %H:%M:%S")):
            datos[conteo] = [alumno.nombres, alumno.id, [i.datetime_touch.strftime("%Y-%m-%d %H:%M:%S"),i.resultado] ]
            conteo += 1



    #Enviar alumno + instancia

    #EN JS: Crear función ligada al boton filtrar
    #ajax a traer_datos pasando el alumno seleccionado
    #Borrar Tabla existente
    #Crear Nueva tabla con los datos obtenidos
    return JsonResponse(datos,safe=False)
#------------------Fin Funcion Evaluacion Propuesta--------------

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
