from collections import OrderedDict

from clases.models import Clase, HorariosClases
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.utils.timezone import datetime, localtime, timedelta
from reservas.models import Reserva

from canchas.forms import FormEditarCancha, FormNuevaCancha
from canchas.models import Cancha, CanchaPrecios, HorariosCancha


def abm_canchas(request):
    if request.method == "GET":
        # busco canchas existentes para mostrar la tabla
        canchas = Cancha.objects.all()
        context = {"canchas": canchas}
        return render(request, "canchas/abm_canchas.html", context)
    else:
        # cambio de estado de cancha
        if "desactivar" in request.POST:
            cancha_id = request.POST.get("desactivar")
            cancha_qs = Cancha.objects.filter(cancha_id=cancha_id)
            cancha_qs.update(activo=False)
            messages.success(request, "¡Cancha desactivada con éxito!")
        else:
            cancha_id = request.POST.get("activar")
            cancha_qs = Cancha.objects.filter(cancha_id=cancha_id)
            cancha_qs.update(activo=True)
            messages.success(request, "¡Cancha activada con éxito!")
        return HttpResponseRedirect(reverse("Canchas"))


def nueva_cancha(request):
    dias = [
        {"dia": "Lunes", "hora": "horaLunes"},
        {"dia": "Martes", "hora": "horaMartes"},
        {"dia": "Miercoles", "hora": "horaMiercoles"},
        {"dia": "Jueves", "hora": "horaJueves"},
        {"dia": "Viernes", "hora": "horaViernes"},
        {"dia": "Sabado", "hora": "horaSabado"},
        {"dia": "Domingo", "hora": "horaDomingo"},
    ]
    if request.method == "GET":
        mi_formulario = FormNuevaCancha()
        context = {
            "form": mi_formulario,
            "dias": dias,
        }
        return render(request, "canchas/nueva_cancha.html", context)

    else:
        # recupero datos del form
        mi_formulario = FormNuevaCancha(request.POST)
        numero = request.POST.get("numero")

        # verificar si ya existe una cancha con ese mismo numero
        if Cancha.objects.filter(numero=numero).exists():
            messages.warning(request, "Ya existe una cancha con ese numero")
            dias = [
                {"dia": "Lunes", "hora": "horaLunes"},
                {"dia": "Martes", "hora": "horaMartes"},
                {"dia": "Miercoles", "hora": "horaMiercoles"},
                {"dia": "Jueves", "hora": "horaJueves"},
                {"dia": "Viernes", "hora": "horaViernes"},
                {"dia": "Sabado", "hora": "horaSabado"},
                {"dia": "Domingo", "hora": "horaDomingo"},
            ]
            context = {
                "form": mi_formulario,
                "dias": dias,
            }
            return render(request, "canchas/nueva_cancha.html", context)

        if mi_formulario.is_valid():
            numero = mi_formulario.cleaned_data["numero"]
            precio = mi_formulario.cleaned_data["precio"]
            # creo nueva cancha y nuevo precio para la cancha
            cancha = Cancha(numero=numero)
            cancha_precio = CanchaPrecios(cancha=cancha, precio=precio)

            # recupero datos del form y elimino lo que no sea parte de los horarios
            datos_formulario = request.POST.dict()

            for key in ["csrfmiddlewaretoken", "numero", "precio"]:
                if key in datos_formulario:
                    del datos_formulario[key]

            # cargo los horarios para la nueva cancha
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    cancha_horario = HorariosCancha(
                        cancha=cancha, dia=dia
                    )  # type:Cancha
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    cancha_horario.hora_desde = datos_formulario.get(desde_key)
                    cancha_horario.hora_hasta = datos_formulario.get(hasta_key)
                    if cancha.validar_horario_limite_club(cancha_horario):
                        # guardo cancha, precio y horario
                        cancha.save()
                        cancha_precio.save()
                        cancha_horario.save()
                    else:
                        messages.error(
                            request, "Error al cargar cancha. Ingrese un horario valido"
                        )
                        context = {
                            "form": mi_formulario,
                            "dias": dias,
                        }
                        return render(request, "canchas/nueva_cancha.html", context)

            messages.success(request, "¡Cancha cargada con éxito!")
            return HttpResponseRedirect(reverse("NuevaCancha"))


def editar_cancha(request, **kwargs):
    dias = OrderedDict()
    dias["Lunes"] = {"obj": None, "hora": "horaLunes"}
    dias["Martes"] = {"obj": None, "hora": "horaMartes"}
    dias["Miercoles"] = {"obj": None, "hora": "horaMiercoles"}
    dias["Jueves"] = {"obj": None, "hora": "horaJueves"}
    dias["Viernes"] = {"obj": None, "hora": "horaViernes"}
    dias["Sabado"] = {"obj": None, "hora": "horaSabado"}
    dias["Domingo"] = {"obj": None, "hora": "horaDomingo"}

    cancha_id = kwargs.get("cancha_id")

    if request.method == "GET":

        # busco datos existentes de la cancha para mostrarlos
        cancha = Cancha.objects.get(cancha_id=kwargs["cancha_id"])
        horarios_qs = HorariosCancha.objects.filter(cancha_id=kwargs["cancha_id"])
        for horario in horarios_qs:
            dias[horario.dia]["obj"] = horario

        datos_iniciales = {
            "precio": cancha.obtener_precio_actual,
            "imagen": cancha.imagen,
        }
        mi_formulario = FormEditarCancha(initial=datos_iniciales)
        context = {
            "form": mi_formulario,
            "dias": dias,
            "cancha": cancha.numero,
        }
        return render(request, "canchas/editar_cancha.html", context)
    else:
        # obtengo datos del form
        mi_formulario = FormEditarCancha(request.POST, request.FILES)
        if mi_formulario.is_valid():
            precio = mi_formulario.cleaned_data["precio"]
            imagen = mi_formulario.cleaned_data["imagen"]

            cancha = Cancha.objects.get(cancha_id=kwargs["cancha_id"])

            if imagen is not None:
                cancha.imagen = imagen

            # obtengo datos del form para actualizar los horarios
            datos_formulario = request.POST.dict()

            # elimino de los datos del form las claves que no sean parte de los horarios
            for key in ["csrfmiddlewaretoken", "numero", "precio"]:
                if key in datos_formulario:
                    del datos_formulario[key]

            lista_horarios_validos = []

            # cargo los nuevos horarios
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    cancha_horario = HorariosCancha(cancha=cancha, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    cancha_horario.hora_desde = datos_formulario.get(desde_key)
                    cancha_horario.hora_hasta = datos_formulario.get(hasta_key)
                    if cancha.validar_horario_limite_club(cancha_horario):
                        if cancha.validar_clase_existente(cancha_horario):
                            lista_horarios_validos.append(cancha_horario)
                        else:
                            messages.error(
                                request,
                                "Error al modificar cancha. El horario ingresado afecta a una clase existente.",
                            )
                            context = {
                                "form": mi_formulario,
                                "dias": dias,
                                "cancha": cancha.numero,
                            }
                            return render(
                                request, "canchas/editar_cancha.html", context
                            )

                    else:
                        messages.error(
                            request,
                            "Error al modificar cancha. Ingrese un horario valido",
                        )
                        context = {
                            "form": mi_formulario,
                            "dias": dias,
                            "cancha": cancha.numero,
                        }
                        return render(request, "canchas/editar_cancha.html", context)

            # guardo cancha, precio y horario
            cancha.save()
            # actualizo precio
            if cancha.obtener_precio_actual() != precio:
                nuevo_precio = CanchaPrecios(cancha=cancha, precio=precio)
                nuevo_precio.save()
            cancha_horario.save()

            if lista_horarios_validos:
                # busco horarios existentes
                horarios_qs = HorariosCancha.objects.filter(
                    cancha_id=kwargs["cancha_id"]
                )
                # borro horarios existentes
                horarios_qs.delete()
                # cargo horarios actualizados
                HorariosCancha.objects.bulk_create(lista_horarios_validos)
            else:
                # busco horarios existentes
                horarios_qs = HorariosCancha.objects.filter(
                    cancha_id=kwargs["cancha_id"]
                )
                # borro horarios existentes
                horarios_qs.delete()

            messages.success(request, "¡Cancha modificada con éxito!")
        else:
            messages.error(request, "Alguno de los datos ingresados no es valido")
        url_destino = reverse("EditarCancha", kwargs={"cancha_id": cancha_id})
        return HttpResponseRedirect(url_destino)


def buscar_canchas(request):
    if request.method == "GET":
        return render(request, "canchas/buscar_canchas.html")
    else:
        fecha_str = request.POST.get("fecha")
        horarios_disponibles = calcular_horarios_disponibles_dia(fecha_str)
        if horarios_disponibles is None:
            messages.error(
                request,
                "Debe ingresar una fecha posterior al dia de hoy y con un formato valido",
            )
            return render(request, "canchas/buscar_canchas.html")
        elif not horarios_disponibles:
            messages.warning(
                request, "No hay horarios disponibles para la fecha ingresada"
            )
            return render(request, "canchas/buscar_canchas.html")
        return render(
            request,
            "canchas/mostrar_canchas.html",
            {
                "horarios_disponibles": horarios_disponibles,
                "fecha": fecha_str,
            },
        )


def calcular_horarios_disponibles_dia(fecha_str):
    try:
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return None
    if fecha_dt <= datetime.now():
        return None
    # busco reservas existentes en esa fecha
    reservas_qs = Reserva.objects.filter(fecha_hora_reserva__date=fecha_dt.date())

    # obtener el día de la semana
    dia_semana_numero = fecha_dt.weekday()

    dias_semana = {
        0: "Lunes",
        1: "Martes",
        2: "Miercoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sabado",
        6: "Domingo",
    }

    horarios_disponibles = []
    intervalo = timedelta(hours=1)

    # busco horarios de canchas en ese dia de la semana
    horarios_canchas_qs = HorariosCancha.objects.select_related("cancha").filter(
        dia=dias_semana[dia_semana_numero],
        cancha__activo=True,
    )

    for horario_cancha in horarios_canchas_qs:
        hora_inicio_limite = horario_cancha.hora_desde
        hora_fin_limite = horario_cancha.hora_hasta

        dia_hora = datetime.combine(fecha_dt.date(), hora_inicio_limite)
        cada_hora = dia_hora.time()

        while cada_hora < hora_fin_limite:
            hay_reserva = False
            for reserva in reservas_qs:
                if reserva.cancha == horario_cancha.cancha:
                    local_dt = localtime(reserva.fecha_hora_reserva)
                    if local_dt.time() == cada_hora:
                        hay_reserva = True
                        break

            if not hay_reserva:
                horarios_disponibles.append(
                    {"hora": cada_hora, "cancha": horario_cancha.cancha}
                )
            dia_hora = dia_hora + intervalo
            cada_hora = dia_hora.time()

    # busco horarios de clases en ese dia de la semana
    horarios_clases_qs = HorariosClases.objects.select_related("clase").filter(
        dia=dias_semana[dia_semana_numero],
        clase__activo=True,
    )

    horarios_disponibles_validados = []

    for horario_disponible in horarios_disponibles:
        hay_clase = False
        for horario_clase in horarios_clases_qs:
            if horario_disponible["cancha"] == horario_clase.clase.cancha:
                if horario_disponible["hora"] == horario_clase.hora_desde:
                    hay_clase = True
                    break

        if not hay_clase:
            horarios_disponibles_validados.append(
                {
                    "hora": horario_disponible["hora"],
                    "cancha": horario_disponible["cancha"],
                }
            )

    return horarios_disponibles_validados
