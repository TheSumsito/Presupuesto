from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from CORE.models import *
from django.contrib.auth.models import User

# ! Utilites
# Genders
class GenderList(generics.ListCreateAPIView):
    queryset = Generos.objects.all()
    serializer_class = GeneroSerializer

# Regiones
class RegionesList(generics.ListCreateAPIView):
    queryset = Regiones.objects.all()
    serializer_class = RegionSerializer

# Provincias
class ProvinciasList(generics.ListCreateAPIView):
    queryset = Provincias.objects.all()
    serializer_class = ProvinciaSerializer



    