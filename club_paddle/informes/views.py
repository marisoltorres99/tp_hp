from django.shortcuts import render
from django.utils.timezone import datetime
from reservas.models import Reserva


def elegir_informe(request):
    if request.method == "GET":
        return render(request, "informes/elegir_informe.html")


def elegir_fecha_canchas_reservadas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")


def elegir_fecha_reservas_canceladas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")
    if request.method == "POST":
        fecha_desde_str = request.POST.get("fechadesde")
        fecha_hasta_str = request.POST.get("fechahasta")

        # convierte las fechas str a fechas date
        fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
        fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()

        # busca las reservas con estado cancelado (C) en el rango de fechas
        reservas_canceladas = Reserva.objects.select_related("cancha").filter(
            estado="C", fecha_hora_reserva__range=[fecha_desde, fecha_hasta]
        )
        cantidad_reservas_canceladas = reservas_canceladas.count()
        context = {
            "reservas_canceladas": reservas_canceladas,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "cantidad_reservas_canceladas": cantidad_reservas_canceladas,
        }
        return render(
            request,
            "informes/reservas_canceladas.html",
            context,
        )


def elegir_fecha_clases_solicitadas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")
