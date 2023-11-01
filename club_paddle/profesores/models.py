from django.db import models


class Profesor(models.Model):
    profesor_id = models.BigAutoField(primary_key=True)
    dni = models.CharField(null=False, blank=False, max_length=8)
    nombre_apellido = models.CharField(null=False, blank=False, max_length=40)
    telefono = models.CharField(null=False, blank=False, max_length=20)
    email = models.EmailField(null=False, blank=False, max_length=30)
    domicilio = models.CharField(null=False, blank=False, max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "profesor"
        verbose_name_plural = "profesores"
        db_table = "profesores"

    def __str__(self):
        return self.nombre_apellido.__str__()

    def mostrar_activo(self):
        return "Activado" if self.activo else "Desactivado"
