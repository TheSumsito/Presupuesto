from django.db import models

# Create your models here.
class Provincia(models.Model):
    IdProvincia=models.IntegerField(primary_key=True)
    NombreProv=models.CharField(max_length=50)

class Comuna(models.Model):
    IdComuna=models.IntegerField(primary_key=True)
    NombreComu=models.CharField(max_length=45)
    Provincia=models.ForeignKey(Provincia, on_delete=True)

class Estado(models.Model):
    IdEstado=models.IntegerField(primary_key=True)
    Descripcion=models.CharField(max_length=45)

class Sucursal(models.Model):
    NombreSuc=models.CharField(primary_key=True, max_length=255)
    Direccion=models.CharField()
    Provincia=models.ForeignKey(Provincia, on_delete=models.CASCADE)
    Comuna=models.ForeignKey(Comuna, on_delete=models.CASCADE)



class Producto(models.Model):
    NombreProd=models.CharField(primary_key=True, max_length=255)
    CantidadProd=models.IntegerField()
    PrecioProd=models.IntegerField()
    Sucursal=models.ForeignKey(Sucursal, on_delete=models.CASCADE)

class Presupuesto(models.Model):
    Nombre=models.ManyToOneRel(Producto, on_delete=models.CASCADE)
    Cantidad=models.IntegerField()
    Saldo=models.IntegerField()
    TotalPagar=models.IntegerField()





class RegistroCompras(models.Model):
    Producto=models.ManyToOneRel(Producto, on_delete=models.CASCADE)
    Estado=models.ForeignKey(Estado, on_delete=models.CASCADE)