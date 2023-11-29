from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render

from canchas.forms import FormNuevaCancha
from canchas.models import Cancha, CanchaPrecios, HorariosCancha


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
            print(request.POST)
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
        "canchas/nueva_cancha.html",
        {
            "form": mi_formulario,
            "dias": dias,
        },
    )
