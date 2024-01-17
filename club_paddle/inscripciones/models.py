from clases.models import Clase
from django.db import models
from usuarios.models import Cliente


class Inscripcion(models.Model):
    inscripcion_id = models.BigAutoField(primary_key=True)
    fecha_hora_inscripcion = models.DateTimeField(null=False, blank=False)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        related_name="inscripciones",
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.RESTRICT,
        related_name="inscripciones",
    )

    class Meta:
        verbose_name = "inscripcion"
        verbose_name_plural = "inscripciones"
        db_table = "inscripciones"

    def __str__(self):
        return self.inscripcion_id.__str__()
