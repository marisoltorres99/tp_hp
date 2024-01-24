from django.urls import path

from . import views

urlpatterns = [
    path("elegir/", views.elegir_informe, name="elegir_informe"),
]
