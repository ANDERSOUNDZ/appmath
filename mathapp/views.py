from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np


# Create your views here.
def indexView(request):
    return render (request,'index.html')

def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro Exitoso')
            return redirect('appmath')
        messages.error(request,'Registro Fallo, Informacion no valida')
    form = NewUserForm
    return render(request,template_name='registro/register.html',context={'register_form':form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Tu estas en una sesion con el nombre {username}.')
                return redirect('index')
            else:
                messages.error(request,'Nombre o contraseña Invalidos')
        else:
            messages.error(request,'Nombre o contraseña Invalidos')
    form = AuthenticationForm()
    return render(request=request, template_name="ingreso/login.html", context={'login_form':form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Tu saliste de tu sesion.')
    return redirect('index')

@login_required
def appmathView(request):
    return render(request,'grafica/mategraph.html')


def result (request):

    a = int(request.GET['a'])
    b = int(request.GET['b'])
    c = int(request.GET['c'])
    x = int(request.GET['x'])
    x = np.linspace(-10, 10, 1000)
    y = a*(x**2) + b*x + c
    figura, ax = plt.subplots()
    ax.plot(x, y)

    buf= io.BytesIO()
    figura.savefig(buf, format="png")
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri= urllib.parse.quote(string)
    return render(request, 'grafica/mategraph.html',{'resultado':uri})