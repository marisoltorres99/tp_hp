from canchas.models import Cancha
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import datetime
from usuarios.models import Cliente

from reservas.models import Reserva


def nueva_reserva(request):
    if request.method == "POST":
        # obtengo cliente
        cliente = Cliente.objects.get(user_id=request.user.id)

        # obtengo cancha
        cancha_id = request.POST.get("confirmar")
        cancha = Cancha.objects.get(cancha_id=cancha_id)

        # obtengo fecha
        fecha_str = request.POST.get("fecha")

        # obtengo hora
        hora_str = request.POST.get("hora")

        fecha_hora_dt = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")

        # Crear nueva reserva
        nueva_reserva = Reserva(
            cliente=cliente,
            fecha_hora_reserva=fecha_hora_dt,
            cancha=cancha,
        )
        nueva_reserva.save()
        messages.success(request, "¡Su reserva ha sido exitosa!")
        return HttpResponseRedirect(reverse("buscar_canchas"))


def mostrar_reservas(request):
    if request.method == "GET":
        cliente = Cliente.objects.get(user_id=request.user.id)
        mis_reservas_qs = Reserva.objects.filter(cliente=cliente)
        context = {"mis_reservas_qs": mis_reservas_qs}
        return render(request, "reservas/mostrar_reservas.html", context)


def cancelar_reserva(request):
    # obtengo reserva
    reserva_id = request.POST.get("reserva")
    reserva = Reserva.objects.get(reserva_id=reserva_id)
    if reserva.se_puede_cancelar:
        reserva.estado = "C"
        reserva.fecha_hora_cance = timezone.now()
        reserva.save()
        messages.success(request, "¡Reserva cancelada con éxito!")
        return HttpResponseRedirect(reverse("mis_reservas"))
