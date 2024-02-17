from collections import OrderedDict

from canchas.models import Cancha
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from inscripciones.models import Inscripcion
from profesores.models import Profesor

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
            clase = Clase.objects.get(clase_id=clase_id)
            if clase.validar_desactivacion():
                clase.activo = False
                clase.save()
                messages.success(request, "¡Clase desactivada con éxito!")
            else:
                messages.error(
                    request,
                    "Error al desactivar clase. Existen inscripciones a la clase.",
                )
        else:
            clase_id = request.POST.get("activar")
            clase = Clase.objects.get(clase_id=clase_id)
            clase.activo = True
            clase.save()
            messages.success(request, "¡Clase activada con éxito!")
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
            cancha = mi_formulario.cleaned_data["cancha"]  # type: Cancha
            # creo nueva clase
            clase = Clase(
                cupo=cupo, descripcion=descripcion, profesor=profesor, cancha=cancha
            )

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
                    if cancha.validar_horario_limite(clase_horario):
                        if cancha.validar_superposicion_clase(clase_horario):
                            if cancha.validar_superposicion_reserva(clase_horario):
                                # guardo clase y horarios
                                if not clase.pk:
                                    clase.save()
                                clase_horario.save()
                            else:
                                mi_formulario = FormNuevaClase(request.POST)
                                context = {
                                    "form": mi_formulario,
                                    "dias": dias,
                                }
                                messages.warning(
                                    request,
                                    "El horario ingresado se superpone con una reserva existente",
                                )
                                return render(
                                    request, "clases/nueva_clase.html", context
                                )
                        else:
                            mi_formulario = FormNuevaClase(request.POST)
                            context = {
                                "form": mi_formulario,
                                "dias": dias,
                            }
                            messages.warning(
                                request,
                                "El horario ingresado se superpone con una clase existente",
                            )
                            return render(request, "clases/nueva_clase.html", context)
                    else:
                        mi_formulario = FormNuevaClase(request.POST)
                        context = {
                            "form": mi_formulario,
                            "dias": dias,
                        }
                        messages.error(request, "Ingrese un horario valido")
                        return render(request, "clases/nueva_clase.html", context)

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
            "clase": clase,
        }
        return render(request, "clases/editar_clase.html", context)
    else:
        # obtengo datos del form
        mi_formulario = FormNuevaClase(request.POST)
        clase = Clase.objects.get(clase_id=kwargs["clase_id"])

        context = {
            "form": mi_formulario,
            "dias": dias,
            "clase": clase,
        }

        if mi_formulario.is_valid():
            cupo = mi_formulario.cleaned_data["cupo"]
            descripcion = mi_formulario.cleaned_data["descripcion"]
            profesor = mi_formulario.cleaned_data["profesor"]
            cancha = mi_formulario.cleaned_data["cancha"]  # type: Cancha

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

            # recupero horarios ingresados
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    clase_horario = HorariosClases(clase=clase, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    clase_horario.hora_desde = datos_formulario.get(desde_key)
                    clase_horario.hora_hasta = datos_formulario.get(hasta_key)
                    dias[dia]["obj"] = clase_horario

            lista_horarios_validos = []

            # cargo los nuevos horarios
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    clase_horario = HorariosClases(clase=clase, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    clase_horario.hora_desde = datos_formulario.get(desde_key)
                    clase_horario.hora_hasta = datos_formulario.get(hasta_key)
                    if cancha.validar_horario_limite(clase_horario):
                        if cancha.validar_superposicion_clase(clase_horario):
                            if cancha.validar_superposicion_reserva(clase_horario):
                                lista_horarios_validos.append(clase_horario)
                            else:
                                mi_formulario = FormNuevaClase(request.POST)
                                messages.error(
                                    request,
                                    "Error al editar clase. El horario ingresado se superpone con una reserva existente",
                                )
                                return render(
                                    request, "clases/editar_clase.html", context
                                )
                        else:
                            mi_formulario = FormNuevaClase(request.POST)
                            messages.error(
                                request,
                                "Error al editar clase. El horario ingresado se superpone con una clase existente",
                            )
                            return render(request, "clases/editar_clase.html", context)
                    else:
                        mi_formulario = FormNuevaClase(request.POST)
                        messages.error(
                            request, "Error al editar clase. Ingrese un horario valido"
                        )
                        return render(request, "clases/editar_clase.html", context)

            # actualizo cupo, descripcion, profesor, cancha y horarios
            clase_id = kwargs["clase_id"]
            clase_qs = Clase.objects.filter(clase_id=clase_id)
            clase_qs.update(
                cupo=cupo,
                descripcion=descripcion,
                profesor=profesor,
                cancha=cancha,
            )

            if lista_horarios_validos:
                # busco horarios existentes
                horarios_qs = HorariosClases.objects.filter(clase_id=kwargs["clase_id"])
                # borro horarios existentes
                horarios_qs.delete()
                # cargo horarios actualizados
                HorariosClases.objects.bulk_create(lista_horarios_validos)
            else:
                # busco horarios existentes
                horarios_qs = HorariosClases.objects.filter(clase_id=kwargs["clase_id"])
                # borro horarios existentes
                horarios_qs.delete()

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
                horarios__dia=dia,
                activo=True,
                cancha__activo=True,
                profesor__activo=True,
            )

            # filtrar las clases que tienen cupo disponible
            clases_con_cupo_disponible = [
                clase for clase in clases_qs if Inscripcion.cupo_disponible(clase)
            ]

        else:
            profesor = request.POST.get("profesor")
            clases_qs = (
                Clase.objects.prefetch_related("horarios")
                .select_related("profesor")
                .filter(
                    profesor=profesor,
                    activo=True,
                    cancha__activo=True,
                    profesor__activo=True,
                )
            )

            # filtrar las clases que tienen cupo disponible
            clases_con_cupo_disponible = [
                clase for clase in clases_qs if Inscripcion.cupo_disponible(clase)
            ]
        if not clases_con_cupo_disponible:
            messages.warning(request, "No se han encontrado clases disponibles")
        return render(
            request,
            "clases/mostrar_clases.html",
            {
                "clases_list": clases_con_cupo_disponible,
            },
        )
