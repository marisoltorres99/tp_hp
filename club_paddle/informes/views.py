from django.shortcuts import render


def elegir_informe(request):
    if request.method == "GET":
        return render(request, "informes/elegir_informe.html")


def elegir_fecha(request):
    if request.method == "GET":
        return render(request, "informes/elegir_fecha.html")
