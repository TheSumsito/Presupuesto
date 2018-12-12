from django.shortcuts import render
from .models import Provincias, Regiones, Usuarios, Productos, Tiendas, Generos, Presupuestos
import json

# OTHERS
from itertools import cycle
import requests

# Login functions
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Net functions
from django.core.mail import EmailMessage
import smtplib
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# ! VALIDATORS AND UTILITES
# Valida Rut
def validarRut(rut):
    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]
    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11
    if str(res) == dv:
        return True
    elif dv == "K" and res == 10:
        return True
    else:
        return False

# Valida Usuario nuevo
def validarUser(newUser):
    usuarios = Usuarios.objects.all()
    for us in usuarios:
        if us.username == newUser:
            return False
    return True

def contacto(request):
    resp = False
    if request.POST:
        name = request.POST.get("txtNombre")
        email = request.POST.get("txtCorreo") 
        mensaje = request.POST.get("txtMensaje")
        # Setea el mensaje
        #ms = "Hola, tienes un mensaje: " + mensaje
        ms="hola, tienes un mensaje:" + mensaje
        # TODO: Crear un correo electronico para la WEB
        fromaddr = 'indigomaker@gmail.com'
        toaddrs = 'rebootsoftware2@gmail.com'
        msg = ms
        username = 'indigomaker@gmail.com'
        password = 'bijuje159951'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        resp = True
        return render(request, 'Views/contacto.htm', {'resp':resp})
    else:
        return render(request, 'Views/contacto.htm', {'resp':resp})

# ! USERS AND LOGINS 
# Login de redes sociales 
def login_social(request):
    return render(request, 'Views/login.htm')

# Login de usuario normal 
def login_usuario(request):
    resp = False
    if request.POST:
        username = request.POST.get("txtUsuario")
        passw = request.POST.get("txtPass")
        user = auth.authenticate(username=username,password=passw)
        if user is not None and user.is_active:
            auth.login(request, user)
            is_admin = request.user.is_staff   
            resp = True     
            return render(request, 'Views/logusuario.htm',{'admin':is_admin, 'user': username, 'resp':resp})
        else:
            resp = False
            is_admin = False
            return render(request, 'Views/logusuario.htm',{'admin':is_admin, 'user': username, 'resp':resp})
    else:
        return render(request, 'Views/logusuario.htm')

# Registro
def registro(request):
    # Obtiene datos 
    resp_gender = requests.get("http://127.0.0.1:8000/api_gen_list/")  
    # Captura el JSON
    genders = resp_gender.json() 
    # Login
    if request.POST:
        rut = request.POST.get("txtRut")
        name = request.POST.get("txtNombre")
        mail = request.POST.get("txtCorreo")
        gender = request.POST.get("cboGenero")
        age = request.POST.get("txtEdad")
        username = request.POST.get("txtUsuario")
        passw = request.POST.get("txtPass")
        passw_con = request.POST.get("txtRepass")
        # DB instances 
        gender_ins = Generos.objects.get(gender_id=gender)
        # ! VALIDACIONES 
        if passw == passw_con:
            if validarRut(rut) == True:
                if validarUser(username) == True:
                    # Crea el nuevo usuario
                    new_user = Usuarios (
                        rut = rut,
                        username = username,
                        passw = passw,
                        name = name,
                        mail = mail,
                        age = age,
                        gender_id = gender_ins,
                    )
                    # Crea al nuevo usuario en la tabla de usuarios 
                    new_user.save()
                    # Crea el nuevo usuario en la tabla auth_user 
                    user_auth = User.objects.create_user(username, mail, passw)
                    user_auth.save()
                    return render(request, 'Views/registro.htm',{'generos': genders, 'succes':True})
                else:
                    return render(request, 'Views/registro.htm',{'generos': genders, 'user_exists':True})
            else:
                return render(request, 'Views/registro.htm',{'generos': genders, 'fake_rut':True})
        else:
            return render(request, 'Views/registro.htm',{'generos': genders, 'no_match':True})
    else:
        return render(request, 'Views/registro.htm',{'generos': genders})
    return render(request, 'Views/registro.htm')

# Logout
@login_required(login_url='/login_usuario')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


def Home(request):
    return render(request, 'Views/home.htm')

def presupuesto(request):
    return render(request, 'Views/presupuesto.htm')

def productos(request):
    return render(request, 'Views/productos.htm')