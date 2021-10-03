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
from django.urls import path,include
from pages.views import home_view, home_reim_view, login_view, logout_view,actividad_view,ayuda_view,lobby_view, crearPreguntas_view, crearAlternativas_view, confirmacion_view, alternativa_view, get_embed_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view , name='home'),
    path('reims/<fecha>/<usuario_id>/<id_colegio>/<id_nivel>/<id_letra>',home_reim_view , name='home_reim'),
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>', lobby_view , name='lobby'),
    path('actividad/<fecha>/<actividad_id>/<id_colegio>/<id_nivel>/<id_letra>', actividad_view, name="actividad"),
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>/preguntas/', crearPreguntas_view, name="crearPregunta"),
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>/preguntas/alternativas', crearAlternativas_view, name="alternativas"),
    path('reim_lobby/<fecha>/<reim_id>/<id_colegio>/<id_nivel>/<id_letra>/preguntas/<id_item>', confirmacion_view, name="confirmacion"),
    path('resultados/', alternativa_view, name="resultados"),
    path('getembedinfo/', get_embed_info),
    path('ayuda/', ayuda_view, name="ayuda"),
    path('login/', login_view, name= "login"),
    url(r'^logout/$', logout_view, name= "logout"),
]
