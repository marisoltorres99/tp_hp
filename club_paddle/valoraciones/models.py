from canchas.models import Cancha
from django.db import models
from usuarios.models import Cliente


class Valoracion(models.Model):
    valoracion_id = models.BigAutoField(primary_key=True)

    valoracion = models.IntegerField()

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        related_name="valoraciones",
    )

    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.RESTRICT,
        related_name="valoraciones",
    )

    class Meta:
        db_table = "valoraciones"
        verbose_name = "valoracion"
        verbose_name_plural = "valoraciones"

    def __str__(self):
        return str(self.valoracion_id)
