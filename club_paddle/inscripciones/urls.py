from django.urls import path

from . import views

urlpatterns = [
    path("", views.abm_profesores, name="Inscripciones"),
    path("nueva/", views.nuevo_profesor, name="NuevaInscripcion"),
]
