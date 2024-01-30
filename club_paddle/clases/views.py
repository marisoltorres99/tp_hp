from collections import OrderedDict

from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from inscripciones.models import Inscripcion
from profesores.models import Profesor
from usuarios.models import Cliente

from clases.forms import FormNuevaClase
from clases.models import Clase, HorariosClases


def abm_clases(request):
    if request.method == "GET":
        # busco clases existentes para mostrar la tabla
        clases = Clase.objects.all()
        context = {"clases": clases}
        return render(request, "clases/abm_clases.html", context)
    else:
        # cambio de estado de clase
        if "desactivar" in request.POST:
            clase_id = request.POST.get("desactivar")
            clase_qs = Clase.objects.filter(clase_id=clase_id)
            clase_qs.update(activo=False)
        else:
            clase_id = request.POST.get("activar")
            clase_qs = Clase.objects.filter(clase_id=clase_id)
            clase_qs.update(activo=True)
        return HttpResponseRedirect(reverse("Clases"))


def nueva_clase(request):
    dias = [
        {"dia": "Lunes", "hora": "horaLunes"},
        {"dia": "Martes", "hora": "horaMartes"},
        {"dia": "Miercoles", "hora": "horaMiercoles"},
        {"dia": "Jueves", "hora": "horaJueves"},
        {"dia": "Viernes", "hora": "horaViernes"},
    ]
    if request.method == "GET":
        mi_formulario = FormNuevaClase()
        context = {
            "form": mi_formulario,
            "dias": dias,
        }
        return render(request, "clases/nueva_clase.html", context)

    else:
        # recupero datos del form
        mi_formulario = FormNuevaClase(request.POST)
        if mi_formulario.is_valid():
            cupo = mi_formulario.cleaned_data["cupo"]
            descripcion = mi_formulario.cleaned_data["descripcion"]
            profesor = mi_formulario.cleaned_data["profesor"]
            cancha = mi_formulario.cleaned_data["cancha"]
            # creo nueva clase
            clase = Clase(
                cupo=cupo, descripcion=descripcion, profesor=profesor, cancha=cancha
            )
            clase.save()

            # recupero datos del form y elimino lo que no sea parte de los horarios
            datos_formulario = request.POST.dict()

            for key in [
                "csrfmiddlewaretoken",
                "cupo",
                "descripcion",
                "profesor",
                "cancha",
            ]:
                if key in datos_formulario:
                    del datos_formulario[key]

            # cargo los horarios para la nueva clase
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    clase_horario = HorariosClases(clase=clase, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    clase_horario.hora_desde = datos_formulario.get(desde_key)
                    clase_horario.hora_hasta = datos_formulario.get(hasta_key)
                    clase_horario.save()

            messages.success(request, "¡Clase cargada con éxito!")
            return HttpResponseRedirect(reverse("NuevaClase"))


def editar_clase(request, **kwargs):
    dias = OrderedDict()
    dias["Lunes"] = {"obj": None, "hora": "horaLunes"}
    dias["Martes"] = {"obj": None, "hora": "horaMartes"}
    dias["Miercoles"] = {"obj": None, "hora": "horaMiercoles"}
    dias["Jueves"] = {"obj": None, "hora": "horaJueves"}
    dias["Viernes"] = {"obj": None, "hora": "horaViernes"}

    if request.method == "GET":
        # busco datos existentes de la clase para mostrarlos
        clase = Clase.objects.get(clase_id=kwargs["clase_id"])

        horarios_qs = HorariosClases.objects.filter(clase_id=kwargs["clase_id"])
        for horario in horarios_qs:
            dias[horario.dia]["obj"] = horario

        datos_iniciales = {
            "cupo": clase.cupo,
            "descripcion": clase.descripcion,
            "profesor": clase.profesor,
            "cancha": clase.cancha,
        }
        mi_formulario = FormNuevaClase(initial=datos_iniciales)
        context = {
            "form": mi_formulario,
            "dias": dias,
        }
        return render(request, "clases/editar_clase.html", context)
    else:
        # obtengo datos del form
        mi_formulario = FormNuevaClase(request.POST)
        if mi_formulario.is_valid():
            cupo = mi_formulario.cleaned_data["cupo"]
            descripcion = mi_formulario.cleaned_data["descripcion"]
            profesor = mi_formulario.cleaned_data["profesor"]
            cancha = mi_formulario.cleaned_data["cancha"]

            # actualizo cupo, descripcion, profesor y cancha
            clase_id = kwargs["clase_id"]
            clase_qs = Clase.objects.filter(clase_id=clase_id)
            clase_qs.update(
                cupo=cupo,
                descripcion=descripcion,
                profesor=profesor,
                cancha=cancha,
            )

            clase = Clase.objects.get(clase_id=kwargs["clase_id"])

            # obtengo datos del form para actualizar los horarios
            datos_formulario = request.POST.dict()

            # elimino de los datos del form las claves que no sean parte de los horarios
            for key in [
                "csrfmiddlewaretoken",
                "cupo",
                "descripcion",
                "profesor",
                "cancha",
            ]:
                if key in datos_formulario:
                    del datos_formulario[key]

            # busco horarios existentes
            horarios_qs = HorariosClases.objects.filter(clase_id=kwargs["clase_id"])

            # borro horarios existentes
            horarios_qs.delete()

            # cargo los nuevos horarios
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    clase_horario = HorariosClases(clase=clase, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    clase_horario.hora_desde = datos_formulario.get(desde_key)
                    clase_horario.hora_hasta = datos_formulario.get(hasta_key)
                    clase_horario.save()

            messages.success(request, "¡Clase modificada con éxito!")
        url_destino = reverse("EditarClase", kwargs={"clase_id": clase_id})
        return HttpResponseRedirect(url_destino)


def buscar_clases(request):
    if request.method == "GET":
        # busco profesores existentes
        profesores = Profesor.objects.all()

        # armo dicc con dias de la semana
        dias = [
            {"dia": "Lunes"},
            {"dia": "Martes"},
            {"dia": "Miercoles"},
            {"dia": "Jueves"},
            {"dia": "Viernes"},
        ]
        context = {
            "profesores": profesores,
            "dias": dias,
        }
        return render(request, "clases/buscar_clases.html", context)
    else:
        criterio_busqueda = request.POST.get("buscar")

        if criterio_busqueda == "dia":
            dia = request.POST.get("dia")

            clases_qs = Clase.objects.prefetch_related("horarios").filter(
                horarios__dia=dia
            )

        else:
            profesor = request.POST.get("profesor")
            clases_qs = (
                Clase.objects.prefetch_related("horarios")
                .select_related("profesor")
                .filter(profesor=profesor)
            )
        return render(
            request,
            "clases/mostrar_clases.html",
            {
                "clases_qs": clases_qs,
            },
        )
