from django.urls import path

from . import views

urlpatterns = [
    path("nueva/", views.nueva_reserva, name="NuevaReserva"),
    path("mis_reservas/", views.mostrar_reservas, name="mis_reservas"),
]
