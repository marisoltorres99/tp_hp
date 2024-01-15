from django.urls import path

from . import views

urlpatterns = [
    path("", views.abm_clases, name="Clases"),
    path("nueva/", views.nueva_clase, name="NuevaClase"),
    path("editar/<int:clase_id>/", views.editar_clase, name="EditarClase"),
    path("buscar/", views.buscar_clases, name="buscar_clases"),
]
