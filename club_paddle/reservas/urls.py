from django.urls import path

from . import views

urlpatterns = [
    path("nueva/", views.nueva_inscripcion, name="NuevaReserva"),
]
