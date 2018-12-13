from django.contrib import admin
from django.urls import path, include
from .views import login_social, cambio_estado, agregar_tienda, eliminar_tienda, login_usuario, Home, contacto, registro, presupuesto, productos, cerrar, recovery, listado, agregar_lista, agregar_tienda_usuario
from API import views

urlpatterns = [
    path('', Home, name="home"),
    path('', include('pwa.urls')),
    path('login/',login_social, name='login'), 
    path('contacto/', contacto, name="contacto"),
    path('registro/', registro, name="registro"),
    path('login_usuario/', login_usuario, name="login_usuario"),
    path('presupuesto/', presupuesto, name="presupuesto"),
    path('agregar_lista/', agregar_lista, name="agregarlista"),
    path('listado/', listado, name="listado"),
    path('productos/', productos, name="productos"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('cerrar/',cerrar, name="cerrar"),
    path('pw_recover/',recovery, name="pw_recover"),

        # ! Vista Usuario agregar tienda
    path('agregar_tienda_usuario/', agregar_tienda_usuario, name="agregar_tienda_usuario"),

    # ! Funciones Administrador
    path('agregar_tienda/', agregar_tienda, name="agregar_tienda"),
    path('eliminar_tienda/', eliminar_tienda, name="eliminar_tienda"),
    path('cambio_estado/', cambio_estado, name="cambio_estado"),

    # ! API 
    path('api_gen_list/', views.GenderList.as_view()),
    path('api_reg_list/', views.RegionesList.as_view()),
    path('api_pro_list/', views.ProvinciasList.as_view()),
]
