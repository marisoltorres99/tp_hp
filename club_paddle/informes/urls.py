from django.urls import path

from . import views

urlpatterns = [
    path("elegir_informe/", views.elegir_informe, name="elegir_informe"),
    path(
        "elegir_fecha_canchas_reservadas/",
        views.elegir_fecha_canchas_reservadas,
        name="elegir_fecha_canchas_reservadas",
    ),
    path(
        "elegir_fecha_reservas_canceladas/",
        views.elegir_fecha_reservas_canceladas,
        name="elegir_fecha_reservas_canceladas",
    ),
    path(
        "elegir_fecha_clases_solicitadas/",
        views.elegir_fecha_clases_solicitadas,
        name="elegir_fecha_clases_solicitadas",
    ),
]
