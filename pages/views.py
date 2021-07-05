from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Actividad

# Create your views here.

def home_view(request,*args, **kwargs):
    return render(request, "pages/home.htm",{})

def home_reim_view(request,*args, **kwargs):
    context = {}
    system = request.POST.get('system',None)
    context['system'] = system
    return render(request, "pages/home_reim.htm",context)

def lobby_view(request,*args, **kwargs):
    context = {}
    reim_escogido = request.POST.get('botonreim',None)
    context['reim_escogido'] = reim_escogido
    return render(request, "Reim1/reim_lobby.htm",context)

def actividad_view(request,mi_id):
    obj = Actividad.objects.get(id_actividad = mi_id)
    context = {
        "object":obj
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
            return redirect('/home')
    else:
        form = AuthenticationForm()
    return render(request, 'Registration/login.html', {'form':form})
    # En vez de form podria pasar el id del usuario, de esa manera en la pagina poder pedir los colegios y cursos del docente

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('../')