from django.urls import path

from . import views

urlpatterns = [
    path("", views.iniciar_sesion, name="iniciar_sesion"),
    path("inicio/", views.inicio, name="inicio"),
    path("registrarse/", views.VRegistro.as_view(), name="registrarse"),
]
