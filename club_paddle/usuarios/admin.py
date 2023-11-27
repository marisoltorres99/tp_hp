from django.contrib import admin

from .models import Administrador, Cliente

admin.site.register(Cliente)

admin.site.register(Administrador)
