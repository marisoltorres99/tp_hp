from django.shortcuts import render


def elegir_informe(request):
    if request.method == "GET":
        return render(request, "informes/elegir_informe.html")


def elegir_fecha_canchas_reservadas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")


def elegir_fecha_reservas_canceladas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")


def elegir_fecha_clases_solicitadas(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")
