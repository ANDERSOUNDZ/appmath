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
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

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
    print('pasa por la funcion')
    a = int(request.GET['a'])
    b = int(request.GET['b'])
    c = int(request.GET['c'])
    # x = np.linspace(10, -10, 100)
    # y = a*(x**2)+b*x+c
    # fig = plt.figure()
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # ax.spines['left'].set_position('center')
    # ax.spines['bottom'].set_position('center')
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # ax.xaxis.set_ticks_position('bottom')   
    # ax.yaxis.set_ticks_position('left')

    #imagen 3d
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    x = np.sqrt(X**2 + Y**2)
    y = a*(x**2)+b*x+c

    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(X, Y, y, rstride=1, cstride=1, cmap=cm.viridis)

    print('pasa 2')
    buf= io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri= urllib.parse.quote(string)
    #return render(request, 'grafica/resultado.html',{'resultado':a,'data':uri})
    return render(request, 'grafica/resultado.html',{'data':uri})

    #plt.plot(x,y, 'g')
    #x = int(request.GET['x'])

    #crear x y_ y
    #fig, ax = plt.subplots()

    #ax.plot([x], [y])
    #como el comportamiento de la linea, y devuelve x negativo , x positivo, Y negativo , y Y positivo
    #ax.plot([1, 2, -3, 5], [1, -5, 2, 3]) 
    #rango
    # x = np.linspace(-10, 10, 1000)
    # y=2*(x**2) + a*x - 2

    # x = range(-10, 15)
    # plt.plot(x, [(i) for i in x])
    # plt.axhline(0, color="black")

    # plt.xlim(-10, 10)
    # plt.ylim(-10, 10)



    # b = int(request.GET['b'])
    # c = int(request.GET['c'])
    # p = int(request.GET['p'])
    # x = np.linspace(-5,5,1)
    # y = a*(x**2)+b*x+c

    #figura = plt.figure()
    # figura, ax = plt.subplots()
    # ax.plot(x, y)
    # ax = figura.add_subplot(1, 1, 1)
    # ax.spines['left'].set_position('center')
    # ax.spines['bottom'].set_position('center')
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # ax.xaxis.set_ticks_position('bottom')   
    # ax.yaxis.set_ticks_position('left')
    # plt.plot(x,y, 'g')