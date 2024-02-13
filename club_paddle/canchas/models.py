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
    numero = models.IntegerField(null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "cancha"
        verbose_name_plural = "canchas"
        db_table = "canchas"

    def __str__(self):
        return str(self.numero)

    def mostrar_activo(self):
        return "Activada" if self.activo else "Desactivada"

    def obtener_precio_actual(self):
        return self.precios.latest("fecha_hora_desde").precio

    def validar_horario(self, horario_ingresado):
        """
        horarios_ingresados = {
            "Lunes": {"desde": "00:00", "hasta": "01:00"},
            "Jueves": {"desde": "03:00", "hasta": "04:00"},
        }
        """
        for horario in self.horarios.all():
            if horario_ingresado.dia == horario.dia:
                # convertir horas y minutos de cadena a objetos datetime
                hora_desde = timezone.datetime.strptime(
                    horario_ingresado.hora_desde, "%H:%M"
                ).time()
                hora_hasta = timezone.datetime.strptime(
                    horario_ingresado.hora_hasta, "%H:%M"
                ).time()
                if hora_desde < horario.hora_desde:
                    return False
                if hora_hasta > horario.hora_hasta:
                    return False
            return True


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
        return str(
            f"Dia: {self.dia} Hora Desde: {self.hora_desde}"
            f"Hora Hasta: {self.hora_hasta} Cancha: {self.cancha}"
        )
