from django.urls import path

from . import views

urlpatterns = [
    path('', views.abm_profesores, name="Profesores"),
    path('nuevo/', views.nuevo_profesor, name="Nuevo"),
    path('editar/<int:profesor_id>/', views.editar_profesor, name="Editar"),
]
