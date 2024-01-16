from django.db import models
from django.utils import timezone


class Cancha(models.Model):
    cancha_id = models.BigAutoField(primary_key=True)
    valoracion = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
    )
    activo = models.BooleanField(default=True)
    numero = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = "cancha"
        verbose_name_plural = "canchas"
        db_table = "canchas"

    def __str__(self):
        return self.numero.__str__()

    def mostrar_activo(self):
        return "Activada" if self.activo else "Desactivada"

    def obtener_precio_actual(self):
        return self.precios.latest("fecha_hora_desde").precio


class CanchaPrecios(models.Model):
    precios_cancha_id = models.BigAutoField(primary_key=True)
    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.RESTRICT,
        related_name="precios",
    )
    precio = models.IntegerField(null=False, blank=False)
    fecha_hora_desde = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "precio"
        verbose_name_plural = "precios"
        db_table = "cancha_precios"

    def __str__(self):
        return self.precios_cancha_id.__str__()


class HorariosCancha(models.Model):
    horarios_cancha_id = models.BigAutoField(primary_key=True)
    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.RESTRICT,
        related_name="horarios",
    )
    dia = models.CharField(
        max_length=10,
        null=False,
        blank=False,
    )
    hora_desde = models.TimeField(
        null=False,
        blank=False,
        auto_now=False,
        auto_now_add=False,
    )
    hora_hasta = models.TimeField(
        null=False,
        blank=False,
        auto_now=False,
        auto_now_add=False,
    )

    class Meta:
        verbose_name = "horario"
        verbose_name_plural = "horarios"
        db_table = "cancha_horarios"

    def __str__(self):
        return self.horarios_cancha_id.__str__()
