from django.urls import path

from apps.canchas import views

urlpatterns = [
    path('', views.listado_canchas),
]
