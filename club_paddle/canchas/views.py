from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render

from canchas.forms import FormNuevaCancha
from canchas.models import Cancha, CanchaPrecios


def abm_canchas(request):
    canchas = Cancha.objects.all()
    return render(request, "canchas/abm_canchas.html", {"canchas": canchas})


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
            messages.success(request, "¡Cancha cargada con éxito!")
            return HttpResponseRedirect("/canchas/nueva/")
    else:
        mi_formulario = FormNuevaCancha()
    return render(
        request,
        "canchas/nueva_cancha.html",
        {"form": mi_formulario},
    )
