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
import shutil
import os

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
        ms = 'Senor admin tienes un mensaje de ' + name + 'de correo' + email + ', dice ' + mensaje
        fromaddr = 'indigomaker@gmail.com'
        toaddrs = 'rebootsoftware2@gmail.com'
        username = 'indigomaker@gmail.com'
        password = 'bijuje159951'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, ms)
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

# Recuperar contraseña
def recovery(request):
    resp = False 
    if request.POST:
        user_to = request.POST.get("txtUsuario")
        name_to = request.POST.get("txtName")
        try:
            reg_user = Usuarios.objects.get(username=user_to, name=name_to)
        except Exception as ex:
            resp = False
            return render(request, 'Views/pw_recover.htm', {'resp':resp, 'not_found':True})
        name = reg_user.username
        passw = reg_user.passw
        correo = reg_user.mail
        # Setea el mensaje
        ms = 'hola ' + str(name) + ' te recordamos que tu password es ' + str(passw)
        fromaddr = 'indigomaker@gmail.com'
        toaddrs = correo
        username = 'indigomaker@gmail.com'
        password = 'bijuje159951'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, ms)
        server.quit()
        resp = True
        return render(request, 'Views/pw_recover.htm', {'resp':resp,'correo':correo})
    else:
        return render(request, 'Views/pw_recover.htm')

# Logout
@login_required(login_url='/login_usuario')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')

# ! FUNCIONALIDAD 
# Lista de presupuestos
@login_required(login_url='/login_usuario')
def presupuesto(request):
    stores = Tiendas.objects.all()
    cur_usu = request.user
    cur_name = cur_usu.username
    cur_user = Usuarios.objects.get(username=cur_name)
    user_rut = cur_user.rut
    user_list = Presupuestos.objects.filter(user_rut=user_rut)
    if request.POST:
        accion = request.POST.get("btnAdd")
        list_n = Presupuestos.objects.get(name=accion)
        prod = Productos.objects.filter(pres_name=list_n)
        return render(request, 'Views/listado.htm', {'cur_user':cur_user,'list_name':list_n, 'user_list':user_list, 'stores':stores, 'productos':prod})
    else:
        return render(request, 'Views/presupuesto.htm', {'cur_user':cur_user, 'user_list':user_list, 'stores':stores})

# Agregar Lista
@login_required(login_url='/login_usuario')
def agregar_lista(request):
    if request.POST:
        name = request.POST.get("txtNombre")
        max_money = request.POST.get("txtTotal")
        cur_usu = request.user
        cur_user = cur_usu.username
        cur_rut = Usuarios.objects.get(username=cur_user)
        pres = Presupuestos(
            name = name,
            tot_prod = 0,
            tot_money = 0,
            max_money = max_money,
            user_rut = cur_rut
        )
        pres.save()
        return render(request, 'Views/listado.htm', {'resp':True, 'cur_list':pres.name})
    else:
        return render(request, 'Views/agregarlista.htm')

# Productos
def productos(request):
    stores = Tiendas.objects.all()
    cur_usu = request.user
    cur_name = cur_usu.username
    cur_user = Usuarios.objects.get(username=cur_name)
    user_rut = cur_user.rut
    user_list = Presupuestos.objects.filter(user_rut=user_rut)
    if request.POST:
        pro_id = 0
        for i in stores:
            pro_id = pro_id + 1
        pro_id = pro_id + 1
        name = request.POST.get("txtNombre")
        store = request.POST.get("cboTienda")
        pre_cost = request.POST.get("txtCosto")
        cost = request.POST.get("txtPrecio")
        notes = request.POST.get("txtNotas")
        # Instances
        store_ins = Tiendas.objects.get(store_id=store) 
        prod = Productos(
            prod_id = pro_id,
            prod_name = name,
            pre_cost = pre_cost,
            real_cost = cost,
            notes = notes,
            store = store_ins,
            pres_name = "lista"
        )
        prod.save() 
        return render(request, 'Views/productos.htm',{'stores':stores,'succes':True, 'lists':user_list})
    else:
        return render(request, 'Views/productos.htm',{'stores':stores, 'lists':user_list})

# Listado
def listado(request, l_name):
    return render(request, 'Views/listado.htm')

def Home(request):
    return render(request, 'Views/home.htm')

def base_layout(request):
    return render(request, 'Complements/head.htm')


# ? vistas administrador CRUD
@login_required(login_url='/login_usuario')
def agregar_tienda(request):
    resp_region = requests.get("http://127.0.0.1:8000/api_reg_list/") 
    resp_provi = requests.get("http://127.0.0.1:8000/api_pro_list/")  
    regions = resp_region.json()
    provinces = resp_provi.json()
    # N de tiendas
    stores = Tiendas.objects.all()
    if request.POST:
        # Add 
        store_id = 0
        for i in stores:
            store_id = store_id + 1
        store_id = store_id + 1
        # name 
        name = request.POST.get("txtNombre")
        office = request.POST.get("txtSucursal")
        address = request.POST.get("txtDireccion")
        city = request.POST.get("cboCiudad")
        region = request.POST.get("cboRegion")
        # Instances
        reg_ins = Regiones.objects.get(region_id=region)
        cit_ins = Provincias.objects.get(provincia_id=city)
        store = Tiendas(
            store_id = store_id,
            store_name = name,
            office = office,
            adress = address,
            provincia_id = cit_ins,
            region_id = reg_ins,
            estado = 1
        )
        store.save()
        return render(request, 'Views/Admin/agregar.htm',{'regiones':regions, 'provincias':provinces, 'succes':True})
    else:
        return render(request, 'Views/Admin/agregar.htm',{'regiones':regions, 'provincias':provinces})

@login_required(login_url='/login_usuario')
def eliminar_tienda(request):
    stores = Tiendas.objects.all()
    if request.POST:
        id_store = request.POST.get("cboTienda")
        store = Tiendas.objects.get(store_id=id_store)
        store.delete()
        return render(request, 'Views/Admin/eliminar.htm', {'stores':stores, 'succes':True})
    else:
        return render(request, 'Views/Admin/eliminar.htm', {'stores':stores})

def cambio_estado(request):
    stores = Tiendas.objects.all()
    if request.POST:
        accion = request.POST.get("btnTest")
        new_tienda = Tiendas.objects.get(store_id=accion)
        new_tienda.estado = 1
        new_tienda.save()
        return render(request, 'Views/Admin/estado.htm', {'stores':stores, 'succes':True})
    else:
        return render(request, 'Views/Admin/estado.htm', {'stores':stores})

def agregar_tienda_usuario(request):
    return render(request, 'Views/agregar_tienda.htm')