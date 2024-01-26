from canchas.models import Cancha
from clases.models import Clase
from django.db.models import Count, Q, Sum
from django.shortcuts import render
from django.utils.timezone import datetime
from reservas.models import Reserva


def elegir_informe(request):
    if request.method == "GET":
        return render(request, "informes/elegir_informe.html")


def elegir_fecha_canchas_reservadas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")
    if request.method == "POST":
        fecha_desde_str = request.POST.get("fechadesde")
        fecha_hasta_str = request.POST.get("fechahasta")

        # convierte las fechas str a fechas date
        fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
        fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()

        # busco canchas reservadas en el periodo de fechas
        reserva_finalizada_segun_fecha = Q(
            reservas__estado="F",
            reservas__fecha_hora_reserva__range=[fecha_desde, fecha_hasta],
        )

        num_reservas = Count(
            "reservas",
            filter=reserva_finalizada_segun_fecha,
        )

        monto_total_historico = Sum(
            "reservas__precio",
            filter=reserva_finalizada_segun_fecha,
        )

        canchas_reservadas = Cancha.objects.annotate(
            num_reservas=num_reservas,
            monto_total_historico=monto_total_historico,
        )

        monto_total_general = canchas_reservadas.aggregate(
            total_monto_general=Sum("monto_total_historico")
        )["total_monto_general"]

        context = {
            "canchas_reservadas": canchas_reservadas,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "monto_total_general": monto_total_general,
        }
        return render(
            request,
            "informes/canchas_reservadas.html",
            context,
        )


def elegir_fecha_reservas_canceladas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")
    if request.method == "POST":
        fecha_desde_str = request.POST.get("fechadesde")
        fecha_hasta_str = request.POST.get("fechahasta")

        # convierte las fechas str a fechas date
        fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
        fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()

        # busco las reservas con estado cancelado (C) en el rango de fechas
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
    if request.method == "POST":
        fecha_desde_str = request.POST.get("fechadesde")
        fecha_hasta_str = request.POST.get("fechahasta")

        # convierte las fechas str a fechas date
        fecha_desde = datetime.strptime(fecha_desde_str, "%Y-%m-%d").date()
        fecha_hasta = datetime.strptime(fecha_hasta_str, "%Y-%m-%d").date()

        clases_solicitadas = Clase.objects.annotate(
            num_inscripciones=Count(
                "inscripciones",
                filter=Q(
                    inscripciones__fecha_hora_inscripcion__range=[
                        fecha_desde,
                        fecha_hasta,
                    ],
                ),
            ),
        ).filter(num_inscripciones__gt=0)

        suma_total_inscripciones = sum(
            clase.num_inscripciones for clase in clases_solicitadas
        )
        context = {
            "clases_solicitadas": clases_solicitadas,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "suma_total_inscripciones": suma_total_inscripciones,
        }
        return render(
            request,
            "informes/clases_solicitadas.html",
            context,
        )
