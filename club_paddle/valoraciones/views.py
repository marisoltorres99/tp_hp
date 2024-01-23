from canchas.models import Cancha
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from usuarios.models import Cliente

from valoraciones.models import Valoracion


def nueva_valoracion(request, cancha_id):
    if request.method == "GET":
        cancha = Cancha.objects.get(cancha_id=cancha_id)
        return render(request, "valoraciones/valorar.html", {"cancha": cancha})
    else:
        valoracion_str = request.POST.get("valoracion")
        valoracion_int = int(valoracion_str)
        cancha = Cancha.objects.get(cancha_id=cancha_id)
        if valoracion_int >= 1 and valoracion_int <= 5:
            cliente = Cliente.objects.get(user_id=request.user.id)
            nueva_val = Valoracion(
                valoracion=valoracion_int,
                cliente=cliente,
                cancha=cancha,
            )
            nueva_val.save()
            messages.success(request, "¡Valoración Registrada!")
            return HttpResponseRedirect(reverse("mis_reservas"))
        else:
            messages.success(request, "Ingrese una valoracion correcta")
            return render(request, "valoraciones/valorar.html", {"cancha": cancha})
