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
        valoracion_cliente = Valoracion.objects.filter(
            cliente_id=request.user.id, cancha=cancha
        ).first()
        if valoracion_cliente is not None:
            mensaje = f"Ya realizo una valoracion para esta cancha. Valoracion actual: {valoracion_cliente.valoracion}. Reemplazar Valoracion:"
        else:
            mensaje = "¡Danos tu opinión! (1 a 5)"
        return render(
            request, "valoraciones/valorar.html", {"cancha": cancha, "mensaje": mensaje}
        )
    else:
        valoracion_str = request.POST.get("valoracion")
        valoracion_int = int(valoracion_str)
        cancha = Cancha.objects.get(cancha_id=cancha_id)
        if valoracion_int >= 1 and valoracion_int <= 5:
            cliente = Cliente.objects.get(user_id=request.user.id)
            valoracion_cliente = Valoracion.objects.filter(
                cliente_id=request.user.id, cancha=cancha
            ).first()
            if valoracion_cliente is None:
                nueva_val = Valoracion(
                    valoracion=valoracion_int,
                    cliente=cliente,
                    cancha=cancha,
                )
                nueva_val.save()
                nueva_val.actualizar_valoracion()
            else:
                valoracion_cliente.valoracion = valoracion_int
                valoracion_cliente.save()
                valoracion_cliente.actualizar_valoracion()

            messages.success(request, "¡Valoración Registrada!")

            return HttpResponseRedirect(reverse("mis_reservas"))
        else:
            messages.success(request, "Ingrese una valoracion correcta")
            return render(request, "valoraciones/valorar.html", {"cancha": cancha})
