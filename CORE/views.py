from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'Views/home.htm')

def login(request):
    return render(request, 'Views/login.htm')

def contacto(request):
    return render(request, 'Views/contacto.htm')

def registro(request):
    return render(request, 'Views/registro.htm')

def login_usuario(request):
    return render(request, 'Views/logusuario.htm')

def presupuesto(request):
    return render(request, 'Views/presupuesto.htm')

def productos(request):
    return render(request, 'Views/productos.htm')