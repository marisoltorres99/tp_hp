from collections import OrderedDict

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
        else:
            cancha_id = request.POST.get("activar")
            cancha_qs = Cancha.objects.filter(cancha_id=cancha_id)
            cancha_qs.update(activo=True)
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
            cancha.save()
            cancha_precio = CanchaPrecios(cancha=cancha, precio=precio)
            cancha_precio.save()

            # recupero datos del form y elimino lo que no sea parte de los horarios
            datos_formulario = request.POST.dict()

            for key in ["csrfmiddlewaretoken", "numero", "precio"]:
                if key in datos_formulario:
                    del datos_formulario[key]

            # cargo los horarios para la nueva cancha
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    cancha_horario = HorariosCancha(cancha=cancha, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    cancha_horario.hora_desde = datos_formulario.get(desde_key)
                    cancha_horario.hora_hasta = datos_formulario.get(hasta_key)
                    cancha_horario.save()

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

    if request.method == "GET":
        # busco datos existentes de la cancha para mostrarlos
        cancha = Cancha.objects.get(cancha_id=kwargs["cancha_id"])

        horarios_qs = HorariosCancha.objects.filter(cancha_id=kwargs["cancha_id"])
        for horario in horarios_qs:
            dias[horario.dia]["obj"] = horario

        datos_iniciales = {
            "precio": cancha.obtener_precio_actual,
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
        mi_formulario = FormEditarCancha(request.POST)
        if mi_formulario.is_valid():
            precio = mi_formulario.cleaned_data["precio"]

            # actualizo precio
            cancha_id = kwargs["cancha_id"]

            cancha = Cancha.objects.get(cancha_id=kwargs["cancha_id"])

            if cancha.obtener_precio_actual() != precio:
                nuevo_precio = CanchaPrecios(cancha=cancha, precio=precio)
                nuevo_precio.save()

            # obtengo datos del form para actualizar los horarios
            datos_formulario = request.POST.dict()

            # elimino de los datos del form las claves que no sean parte de los horarios
            for key in ["csrfmiddlewaretoken", "numero", "precio"]:
                if key in datos_formulario:
                    del datos_formulario[key]

            # busco horarios existentes
            horarios_qs = HorariosCancha.objects.filter(cancha_id=kwargs["cancha_id"])

            # borro horarios existentes
            horarios_qs.delete()

            # cargo los nuevos horarios
            for dia, valor in datos_formulario.items():
                if valor == "on":
                    cancha_horario = HorariosCancha(cancha=cancha, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    cancha_horario.hora_desde = datos_formulario.get(desde_key)
                    cancha_horario.hora_hasta = datos_formulario.get(hasta_key)
                    cancha_horario.save()

            messages.success(request, "¡Cancha modificada con éxito!")
        url_destino = reverse("EditarCancha", kwargs={"cancha_id": cancha_id})
        return HttpResponseRedirect(url_destino)


def buscar_canchas(request):
    if request.method == "GET":
        return render(request, "canchas/buscar_canchas.html")
    else:
        fecha_str = request.POST.get("fecha")
        horarios_disponibles = calcular_horarios_disponibles(fecha_str)
        if not horarios_disponibles:
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


def calcular_horarios_disponibles(fecha_str):
    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")

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

    horarios_qs = HorariosCancha.objects.select_related("cancha").filter(
        dia=dias_semana[dia_semana_numero]
    )

    for horario in horarios_qs:
        hora_inicio = horario.hora_desde
        hora_fin = horario.hora_hasta

        dia_hora = datetime.combine(fecha_dt.date(), hora_inicio)
        cada_hora = dia_hora.time()

        while cada_hora < hora_fin:
            hay_reserva = False
            for reserva in reservas_qs:
                if reserva.cancha == horario.cancha:
                    local_dt = localtime(reserva.fecha_hora_reserva)
                    if local_dt.time() == cada_hora:
                        hay_reserva = True
                        break

            if not hay_reserva:
                horarios_disponibles.append(
                    {"hora": cada_hora, "cancha": horario.cancha}
                )
            dia_hora = dia_hora + intervalo
            cada_hora = dia_hora.time()

    return horarios_disponibles
