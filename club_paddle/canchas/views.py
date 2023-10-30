from django.shortcuts import render

from canchas.models import Cancha


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
    return render(request, "canchas/nueva_cancha.html", {"dias": dias})
