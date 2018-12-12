from django.contrib.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from API import views

urlpatterns = [
    path('lista_provincia', views.ProvinciaList.as_view()),
]
