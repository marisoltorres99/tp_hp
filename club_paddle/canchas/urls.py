from django.urls import path

from . import views

urlpatterns = [
    path('', views.abm_canchas, name="Canchas"),
]
