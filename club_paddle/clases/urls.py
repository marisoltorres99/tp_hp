from django.urls import path

from . import views

urlpatterns = [
    path("", views.abm_clases, name="Clases"),
    path("nueva/", views.nueva_clase, name="Nueva"),
    path("editar/<int:clase_id>/", views.editar_cancha, name="EditarClase"),
]
