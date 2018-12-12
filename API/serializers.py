from rest_framework import serializers
from .models import *
from django_contrib.auth.models import User

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Provincia
        field=('IdProvincia', 'NombreProv')

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comuna
        field=('IdComuna', 'NombreComu', 'Provincia')

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Estado
        field=('IdEstado', 'Descripcion')

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sucursal
        field=('NombreSuc', 'Direccion', 'Provincia', 'Comuna')

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        field=('NombreProd', 'CantidadProd', 'PrecioProd', 'Sucursal')

class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Presupuesto
        field=('Nombre', 'Cantidad', 'Saldo', 'TotalPagar')

class RegistroComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegistroCompras
        field=('Producto', 'Estado')