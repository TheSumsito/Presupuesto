from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('/login/', views.login, name='login'), 
    path('/contacto/', views.contacto, name="contacto"),
    path('/registro/', views.registro, name="registro"),
    path('/login_usuario/', views.login_usuario, name="login_usuario"),
    path('/presupuesto/', views.presupuesto, name="presupuesto"),
    path('/productos/', views.productos, name="productos"),

    path('oauth/', include('social_django.urls', namespace='social')),
]
