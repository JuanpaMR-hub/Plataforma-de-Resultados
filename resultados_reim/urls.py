"""resultados_reim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from pages.views import home_view,guardar_curso, home_reim_view,home_reim_ajax ,login_view, logout_view,ayuda_view, crearPreguntas_view, crearAlternativas_view, confirmacion_view, alternativa_view, contenido_view,  revisar_dibujo_view, traer_dibujos, respuesta_docente, get_embed_info, evaluacionPropuesta_view, guardarCalificacion,traer_datos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view , name='home'),
    path('home_ajax/', guardar_curso, name="home_ajax"),
    path('reims/',home_reim_view , name='home_reim'),
    path('home_reim_ajax/', home_reim_ajax, name="home_reim_ajax"),
    path('resultados/<reim_id>', alternativa_view, name="resultados"),
    path('contenido/', contenido_view, name="contenido"),
    path('getembedinfo/', get_embed_info),
    # Función Crear Preguntas
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>/preguntas/', crearPreguntas_view, name="crearPregunta"),
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>/preguntas/alternativas', crearAlternativas_view, name="alternativas"),
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>/preguntas/<id_item>', confirmacion_view, name="confirmacion"),
    
    #Función Revisar Dibujo
    path('revisionDibujo/<actividad_id>', revisar_dibujo_view, name="RevisarDibujo"),
    path('traer_dibujos/', traer_dibujos),
    path('respuesta_docente/', respuesta_docente),

    #Función Evaluación Propuesta
    path('evaluacionPropuesta', evaluacionPropuesta_view, name="evaluacionPropuesta"),
    path('guardarCalificacion/', guardarCalificacion),
    path('traer_datos/', traer_datos),
    
    path('ayuda/', ayuda_view, name="ayuda"),
    path('login/', login_view, name= "login"),
    url(r'^logout/$', logout_view, name= "logout"),
]
