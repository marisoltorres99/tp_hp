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
    imagen = models.ImageField(upload_to="canchas/images", blank=True, null=True)

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

    def validar_superposicion_clase(self, horario_ingresado):
        clases_qs = self.clases.exclude(clase_id=horario_ingresado.clase.clase_id)
        for clase in clases_qs:
            horarios_qs = clase.horarios.all()
            for horario in horarios_qs:
                if horario_ingresado.dia == horario.dia:
                    # convertir horas y minutos de cadena a objetos datetime
                    hora_desde = timezone.datetime.strptime(
                        horario_ingresado.hora_desde, "%H:%M"
                    ).time()
                    hora_hasta = timezone.datetime.strptime(
                        horario_ingresado.hora_hasta, "%H:%M"
                    ).time()
                    if (
                        hora_desde >= horario.hora_desde
                        and hora_desde <= horario.hora_desde
                    ):
                        return False
                    if (
                        hora_hasta >= horario.hora_hasta
                        and hora_hasta <= horario.hora_hasta
                    ):
                        return False
        return True

    def validar_superposicion_reserva(self, horario_ingresado):
        dias_semana = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo",
        }
        reservas_qs = self.reservas.filter(estado="P")
        for reserva in reservas_qs:
            dia_semana_numero = reserva.fecha_hora_reserva.weekday()
            nombre_dia_semana = dias_semana[dia_semana_numero]
            if horario_ingresado.dia == nombre_dia_semana:
                hora_reserva = timezone.datetime.combine(
                    reserva.fecha_hora_reserva.date(), reserva.fecha_hora_reserva.time()
                )
                # convertir horas y minutos de cadena a objetos datetime
                hora_desde = timezone.datetime.strptime(
                    horario_ingresado.hora_desde, "%H:%M"
                ).time()
                hora_hasta = timezone.datetime.strptime(
                    horario_ingresado.hora_hasta, "%H:%M"
                ).time()
                hora_desde_dt = timezone.datetime.combine(
                    reserva.fecha_hora_reserva.date(), hora_desde
                )
                hora_hasta_dt = timezone.datetime.combine(
                    reserva.fecha_hora_reserva.date(), hora_hasta
                )
                if (
                    hora_desde_dt <= hora_reserva <= hora_hasta_dt
                    or hora_desde_dt
                    <= hora_reserva + timezone.timedelta(hours=1)
                    <= hora_hasta_dt
                ):
                    return False

        return True

    def validar_horario_limite(self, horario_ingresado):
        lista_dias = self.horarios.all().values_list("dia", flat=True)
        if horario_ingresado.dia not in lista_dias:
            return False

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
