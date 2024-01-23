from django.urls import path

from . import views

urlpatterns = [
    path("valorar/<int:cancha_id>/", views.nueva_valoracion, name="nueva_valoracion"),
]
