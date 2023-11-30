from django.urls import path

from . import views

urlpatterns = [
    path("", views.abm_canchas, name="Canchas"),
    path("nueva/", views.nueva_cancha, name="Nueva"),
    path("editar/<int:cancha_id>/", views.editar_cancha, name="EditarCancha"),
]
