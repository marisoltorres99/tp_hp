from django.shortcuts import render

from canchas.models import Cancha


def abm_canchas(request):
    canchas=Cancha.objects.all()
    return render(request, "canchas/abm_canchas.html", {"canchas":canchas})

def nueva_cancha(request):
    rango = range(1,7)
    return render(request, "canchas/nueva_cancha.html", {"rango":rango})
