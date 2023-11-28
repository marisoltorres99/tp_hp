"""
URL configuration for club_paddle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from usuarios.views import cerrar_sesion, iniciar_sesion

urlpatterns = [
    path("", iniciar_sesion),
    path("admin/", admin.site.urls),
    path("canchas/", include("canchas.urls")),
    path("profesores/", include("profesores.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("iniciar_sesion/", iniciar_sesion, name="iniciar_sesion"),
    path("cerrar_sesion/", cerrar_sesion, name="cerrar_sesion"),
]
