from django.urls import path

from . import views

urlpatterns = [
    path("menu_principal/", views.menu_principal, name="menu_principal"),
    path("registrarse/", views.VRegistro.as_view(), name="registrarse"),
    path("mi_cuenta/", views.mi_cuenta, name="mi_cuenta"),
    path("modificar_cuenta/", views.modificar_cuenta, name="modificar_cuenta"),
    path("modificar_password/", views.change_password, name="modificar_password"),
]
