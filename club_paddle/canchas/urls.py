from django.urls import path

from . import views

urlpatterns = [
    path('', views.abm_canchas, name="Canchas"),
    path('nueva/', views.nueva_cancha, name="Nueva"),
]
