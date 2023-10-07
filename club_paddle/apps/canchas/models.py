from django.db import models


class Cancha(models.Model):
    cancha_id = models.BigAutoField(primary_key=True)
    numero = models.IntegerField(blank=False, null=False)
    valoracion = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta():
        db_table = "canchas"
        verbose_name = "cancha"
        verbose_name_plural = "canchas"
