from django.urls import path

from . import views

urlpatterns = [
    path("elegir/", views.elegir_informe, name="elegir_informe"),
    path("elegir_fecha/", views.elegir_fecha, name="elegir_fecha"),
]
