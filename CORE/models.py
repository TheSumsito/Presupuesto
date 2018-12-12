from django.db import models

# ! Utilites
# Regiones 
class Regiones(models.Model):
    region_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, verbose_name="region", default="nn") 
    ordinal = models.CharField(max_length=3, default="I")
    def __str__(self):
        return self.ordinal

# Provincias
class Provincias(models.Model):
    provincia_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, verbose_name="provincia", default="nn")
    region_id = models.ForeignKey(Regiones, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre 

# Generos 
class Generos(models.Model):
    gender_id = models.IntegerField(primary_key=True)
    gender_desc = models.CharField(max_length=20, verbose_name="gender_desc")
    def __str__(self):
        return self.gender_desc

# ! Users
# Usuarios 
class Usuarios(models.Model):
    rut = models.CharField(max_length=12, default="nn", primary_key=True)
    username = models.CharField(max_length=20, default="nn")
    passw = models.CharField(max_length=20, default="nn")
    name = models.CharField(max_length=20, default="nn")
    mail = models.CharField(max_length=20, default="nn")
    gender_id = models.ForeignKey(Generos, on_delete=models.CASCADE)
    age = models.IntegerField()
    def __str__(self):
        return self.name

# ! Product and store
# Tiendas
class Tiendas(models.Model):
    store_id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=20, default="nn")
    office = models.CharField(max_length=20, default="nn")
    adress = models.CharField(max_length=20, default="nn")
    region_id = models.ForeignKey(Regiones, on_delete=models.CASCADE)
    provincia_id = models.ForeignKey(Provincias, on_delete=models.CASCADE)
    def __str__(self):
        return self.store_name

# Presupuestos 
class Presupuestos(models.Model):
    name = models.CharField(primary_key=True, max_length=20, default="nn")
    user_rut = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    tot_prod = models.IntegerField()
    tot_money = models.IntegerField()
    max_money = models.IntegerField()
    def __str__(self):
        return self.name

# Productos
class Productos(models.Model):
    prod_id = models.IntegerField(primary_key=True)
    pres_name = models.ForeignKey(Presupuestos, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=20, default="name")
    pre_cost = models.IntegerField()
    real_cost = models.IntegerField()
    notes = models.CharField(max_length=40, default="nodesc")
    def __str__(self):
        return self.prod_name 



