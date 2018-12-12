from rest_framework import serializers
from CORE.models import Provincias, Regiones, Usuarios, Productos, Tiendas, Generos, Presupuestos

# ! Utilites
# Provincias
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincias
        fields = ('provincia_id', 'nombre', 'region_id_id')

# Regiones 
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiones
        fields = ('region_id', 'nombre', 'ordinal')

# Generos
class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generos
        fields = ('gender_id', 'gender_desc')