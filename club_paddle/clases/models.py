from canchas.models import Cancha
from django.db import models
from profesores.models import Profesor


class Clase(models.Model):
    clase_id = models.BigAutoField(primary_key=True)
    cupo = models.IntegerField(null=False, blank=False)
    descripcion = models.CharField(max_length=40)
    activo = models.BooleanField(default=True)
    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.RESTRICT,
        related_name="clases",
    )
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.RESTRICT,
        related_name="clases",
    )

    class Meta:
        verbose_name = "clase"
        verbose_name_plural = "clases"
        db_table = "clases"

    def __str__(self):
        return self.clase_id.__str__()

    def mostrar_activo(self):
        return "Activada" if self.activo else "Desactivada"

    def validar_desactivacion(self):
        inscripciones_qs = self.inscripciones.all()
        if inscripciones_qs.exists():
            # hay inscripciones, por lo tanto, no se puede desactivar
            return False
        # no hay inscripciones, por lo tanto, puede desactivarse
        return True


class HorariosClases(models.Model):
    horarios_clase_id = models.BigAutoField(primary_key=True)
    clase = models.ForeignKey(
        Clase,
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
        db_table = "clase_horarios"

    def __str__(self):
        return self.horarios_clase_id.__str__()
