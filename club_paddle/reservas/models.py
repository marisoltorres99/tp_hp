from canchas.models import Cancha
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from usuarios.models import Cliente


class Reserva(models.Model):
    class Estados(models.TextChoices):
        FINALIZADA = "F", _("Finalizada")
        PENDIENTE = "P", _("Pendiente")
        CANCELADA = "C", _("Cancelada")

    reserva_id = models.BigAutoField(primary_key=True)

    fecha_hora_reserva = models.DateTimeField()

    estado = models.CharField(
        max_length=2,
        choices=Estados.choices,
        default=Estados.PENDIENTE,
    )

    pagada = models.BooleanField(default=False)

    fecha_hora_cance = models.DateTimeField(null=True, blank=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        related_name="reservas",
    )

    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.RESTRICT,
        related_name="reservas",
    )

    class Meta:
        db_table = "reservas"
        verbose_name = "reserva"
        verbose_name_plural = "reservas"

    def __str__(self):
        return self.reserva_id.__str__()

    def se_puede_cancelar(self):
        fecha_hora_limite = timezone.now() + timezone.timedelta(hours=48)
        return self.fecha_hora_reserva >= fecha_hora_limite

    def se_puede_valorar(self):
        return self.fecha_hora_reserva <= timezone.now()
