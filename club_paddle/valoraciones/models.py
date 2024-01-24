from canchas.models import Cancha
from django.db import models
from django.db.models import Sum
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

    def actualizar_valoracion(self):
        valoraciones_cancha_qs = Valoracion.objects.filter(cancha=self.cancha)

        # calcular la suma de las valoraciones
        suma_valoraciones = (
            valoraciones_cancha_qs.aggregate(Sum("valoracion"))["valoracion__sum"] or 0
        )

        # calcular la cantidad total de valoraciones
        cantidad_valoraciones = (
            valoraciones_cancha_qs.count() or 1
        )  # evitar la división por cero

        # calcular el promedio de las valoraciones
        promedio_valoraciones = suma_valoraciones / cantidad_valoraciones

        # actualizar el atributo de la cancha con el promedio
        self.cancha.valoracion = promedio_valoraciones
        self.cancha.save()
