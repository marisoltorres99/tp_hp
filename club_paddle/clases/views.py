from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from clases.forms import FormNuevaClase
from clases.models import Clase, HorariosClases


def abm_clases(request):
    if request.method == "GET":
        clases = Clase.objects.all()
        context = {"clases": clases}
        return render(request, "clases/abm_clases.html", context)
    else:
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
        {"dia": "Sabado", "hora": "horaSabado"},
        {"dia": "Domingo", "hora": "horaDomingo"},
    ]
    if request.method == "POST":
        mi_formulario = FormNuevaClase(request.POST)
        if mi_formulario.is_valid():
            cupo = mi_formulario.cleaned_data["cupo"]
            descripcion = mi_formulario.cleaned_data["descripcion"]
            profesor = mi_formulario.cleaned_data["profesor"]
            cancha = mi_formulario.cleaned_data["cancha"]
            clase = Clase(
                cupo=cupo, descripcion=descripcion, profesor=profesor, cancha=cancha
            )
            clase.save()

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

            for dia, valor in datos_formulario.items():
                if valor == "on":
                    clase_horario = HorariosClases(clase=clase, dia=dia)
                    desde_key = f"hora{dia}_desde"
                    hasta_key = f"hora{dia}_hasta"
                    clase_horario.hora_desde = datos_formulario.get(desde_key)
                    clase_horario.hora_hasta = datos_formulario.get(hasta_key)
                    clase_horario.save()

            messages.success(request, "¡Clase cargada con éxito!")
            return HttpResponseRedirect("/clases/nueva/")
    else:
        mi_formulario = FormNuevaClase()
    return render(
        request,
        "clases/form_clase.html",
        {
            "form": mi_formulario,
            "dias": dias,
            "boton_submit": "Cargar",
            "abm": "Nueva Clase",
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
