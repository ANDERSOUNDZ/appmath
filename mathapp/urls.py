from django.urls import path
from django.contrib.auth import login, authenticate, logout
from .views import indexView, register_request, login_request, logout_request, appmathView, result

urlpatterns = [
    path('',indexView, name='index'),
    path('appgrap',appmathView,name='appmath'),
    path('result',result, name='result'),
    path('register',register_request,name='register'),
    path('login',login_request, name='login'),
    path('logout',logout_request, name='logout')
]
