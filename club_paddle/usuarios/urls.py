from django.urls import path

from . import views

urlpatterns = [
    path("menu_principal/", views.menu_principal, name="menu_principal"),
    path("registrarse/", views.VRegistro.as_view(), name="registrarse"),
]
