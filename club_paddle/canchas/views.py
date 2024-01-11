from collections import OrderedDict

from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from canchas.forms import FormNuevaCancha
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
            "numero": cancha.numero,
            "precio": cancha.obtener_precio_actual,
        }
        mi_formulario = FormNuevaCancha(initial=datos_iniciales)
        context = {
            "form": mi_formulario,
            "dias": dias,
        }
        return render(request, "canchas/editar_cancha.html", context)
    else:
        # obtengo datos del form
        mi_formulario = FormNuevaCancha(request.POST)
        if mi_formulario.is_valid():
            numero = mi_formulario.cleaned_data["numero"]
            precio = mi_formulario.cleaned_data["precio"]

            # actualizo numero y precio
            cancha_id = kwargs["cancha_id"]
            cancha_qs = Cancha.objects.filter(cancha_id=cancha_id)
            cancha_qs.update(numero=numero)

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
