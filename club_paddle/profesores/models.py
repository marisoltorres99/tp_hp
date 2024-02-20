from django.db import models
from django.utils import timezone


class Profesor(models.Model):
    profesor_id = models.BigAutoField(primary_key=True)
    dni = models.CharField(null=False, blank=False, max_length=8)
    nombre_apellido = models.CharField(null=False, blank=False, max_length=40)
    telefono = models.CharField(null=False, blank=False, max_length=20)
    email = models.EmailField(null=False, blank=False, max_length=30)
    domicilio = models.CharField(null=False, blank=False, max_length=20)
    activo = models.BooleanField(default=True)

    def validar_desactivacion(self):
        clases_qs = self.clases.all()
        if clases_qs.exists():
            # si hay clases asociadas al profesor
            for clase in clases_qs:
                if clase.inscripciones.exists():
                    # si hay inscripciones en alguna de las clases del profesor
                    return False
        # no hay inscripciones en ninguna de las clases del profesor
        return True

    def validar_existencia_clase_horario(self, horario_ingresado):
        dia = horario_ingresado.dia
        hora_desde_str = horario_ingresado.hora_desde
        hora_hasta_str = horario_ingresado.hora_hasta

        # convertir las cadenas de tiempo a objetos time
        hora_desde = timezone.datetime.strptime(hora_desde_str, "%H:%M").time()
        hora_hasta = timezone.datetime.strptime(hora_hasta_str, "%H:%M").time()

        # buscar todas las clases del profesor para el día dado
        clases_profesor = self.clases.exclude(
            clase_id=horario_ingresado.clase.clase_id
        ).filter(horarios__dia=dia)

        for clase in clases_profesor:
            # obtener los horarios asociados a la clase
            horarios_clase = clase.horarios.all()

            for horario in horarios_clase:
                # verificar si hay solapamiento de horarios
                if (
                    (
                        hora_desde >= horario.hora_desde
                        and hora_desde < horario.hora_hasta
                    )
                    or (
                        hora_hasta > horario.hora_desde
                        and hora_hasta <= horario.hora_hasta
                    )
                    or (
                        hora_desde <= horario.hora_desde
                        and hora_hasta >= horario.hora_hasta
                    )
                ):
                    return False

        return True

    class Meta:
        verbose_name = "profesor"
        verbose_name_plural = "profesores"
        db_table = "profesores"

    def __str__(self):
        return self.nombre_apellido.__str__()

    def mostrar_activo(self):
        return "Activado" if self.activo else "Desactivado"
