from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
from django.contrib.auth.models import User

# Create your views here.
#! Listar - Ingresar
class ProvinciaList(generics.ListCreateAPIView):
    queryset=Provincia.objects.all()
    serializer_class=ProvinciaSerializer

class ComunaList(generics.ListCreateAPIView):
    queryset=Comuna.objects.all()
    serializer_class=ComunaSerializer

class EstadoList(generics.ListCreateAPIView):
    queryset=Estado.objects.all()
    serializer_class=EstadoSerializer

class SucursalList(generics.ListCreateAPIView):
    queryset=Sucursal.objects.all()
    serializer_class=SucursalSerializer

class ProductoList(generics.ListCreateAPIView):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer

class PresupuestoList(generics.ListCreateAPIView):
    queryset=Presupuesto.objects.all()
    serializer_class=PresupuestoSerializer

class RegistroComprasList(generics.ListCreateAPIView):
    queryset=RegistroCompras.objects.all()
    serializer_class=RegistroComprasSerializer

#! Modificar - Eliminar - Buscar
class ProvinciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Provincia.objects.all()
    serializer_class=ProvinciaSerializer

class ComunaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comuna.objects.all()
    serializer_class=ComunaSerializer

class EstadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Estado.objects.all()
    serializer_class=EstadoSerializer

class SucursalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Sucursal.objects.all()
    serializer_class=SucursalSerializer

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer

class PresupuestoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Presupuesto.objects.all()
    serializer_class=PresupuestoSerializer

class RegistroComprasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=RegistroCompras.objects.all()
    serializer_class=RegistroComprasSerializer

    