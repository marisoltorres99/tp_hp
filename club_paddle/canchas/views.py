from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from canchas.forms import FormNuevaCancha
from canchas.models import Cancha, CanchaPrecios, HorariosCancha


def abm_canchas(request):
    if request.method == "GET":
        canchas = Cancha.objects.all()
        context = {"canchas": canchas}
        return render(request, "canchas/abm_canchas.html", context)
    else:
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
    if request.method == "POST":
        mi_formulario = FormNuevaCancha(request.POST)
        if mi_formulario.is_valid():
            numero = mi_formulario.cleaned_data["numero"]
            precio = mi_formulario.cleaned_data["precio"]
            cancha = Cancha(numero=numero)
            cancha.save()
            cancha_precio = CanchaPrecios(cancha=cancha, precio=precio)
            cancha_precio.save()

            datos_formulario = request.POST.dict()

            for key in ["csrfmiddlewaretoken", "numero", "precio"]:
                if key in datos_formulario:
                    del datos_formulario[key]

            for dia, valor in datos_formulario.items():
                if valor == "on":
                    cancha_horario = HorariosCancha(cancha=cancha, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    cancha_horario.hora_desde = datos_formulario.get(desde_key)
                    cancha_horario.hora_hasta = datos_formulario.get(hasta_key)
                    cancha_horario.save()

            messages.success(request, "¡Cancha cargada con éxito!")
            return HttpResponseRedirect("/canchas/nueva/")
    else:
        mi_formulario = FormNuevaCancha()
    return render(
        request,
        "canchas/form_cancha.html",
        {
            "form": mi_formulario,
            "dias": dias,
            "boton_submit": "Cargar",
            "abm": "Nueva Cancha",
        },
    )


def editar_cancha(request, **kwargs):
    if request.method == "GET":
        cancha = Cancha.objects.get(cancha_id=kwargs["cancha_id"])
        datos_iniciales = {
            "numero": cancha.numero,
            "precio": cancha.obtener_precio_actual,
        }
        mi_formulario = FormNuevaCancha(initial=datos_iniciales)
        context = {
            "form": mi_formulario,
            "boton_submit": "Modificar",
            "abm": "Editar Cancha",
        }
        return render(request, "canchas/form_cancha.html", context)
    else:
        mi_formulario = FormNuevaCancha(request.POST)
        if mi_formulario.is_valid():
            numero = mi_formulario.cleaned_data["numero"]
            precio = mi_formulario.cleaned_data["precio"]

            cancha_id = kwargs["cancha_id"]
            cancha_qs = Cancha.objects.filter(cancha_id=cancha_id)
            cancha_qs.update(numero=numero)

            cancha = Cancha.objects.get(cancha_id=kwargs["cancha_id"])
            nuevo_precio = CanchaPrecios(cancha=cancha, precio=precio)
            nuevo_precio.save()

            messages.success(request, "¡Cancha modificada con éxito!")
        url_destino = reverse("EditarCancha", kwargs={"cancha_id": cancha_id})
        return HttpResponseRedirect(url_destino)
