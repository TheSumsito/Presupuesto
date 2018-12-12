from django.contrib import admin
from django.urls import path, include
from .views import login_social, login_usuario, Home, contacto, registro, presupuesto, productos, cerrar
from API import views

urlpatterns = [
    path('', Home, name="home"),
    path('login/',login_social, name='login'), 
    path('contacto/', contacto, name="contacto"),
    path('registro/', registro, name="registro"),
    path('login_usuario/', login_usuario, name="login_usuario"),
    path('presupuesto/', presupuesto, name="presupuesto"),
    path('productos/', productos, name="productos"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('cerrar/',cerrar, name="cerrar"),

    # ! API 
    path('api_gen_list/', views.GenderList.as_view()),
    path('api_reg_list/', views.RegionesList.as_view()),
    path('api_pro_list/', views.ProvinciasList.as_view()),
]
