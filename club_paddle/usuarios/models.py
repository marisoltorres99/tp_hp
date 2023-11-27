from django.contrib.auth.models import User
from django.db import models


class Cliente(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8)
    domicilio = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        db_table = "clientes"


class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8)

    class Meta:
        verbose_name = "administrador"
        verbose_name_plural = "administradores"
        db_table = "administradores"
