from django.db import models


class Cancha(models.Model):
    cancha_id = models.BigAutoField(primary_key=True)
    valoracion = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    activo = models.BooleanField(default=True)
    numero = models.IntegerField()

    class Meta:
        verbose_name="cancha"
        verbose_name_plural="canchas"
        db_table="canchas"

    def __str__(self):
        return self.numero.__str__()

