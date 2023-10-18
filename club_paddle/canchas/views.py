from django.shortcuts import render

from canchas.models import Cancha, Precios_cancha


def abm_canchas(request):
    canchas=Cancha.objects.all()
    precios=Precios_cancha.objects.all()
    return render(request, "canchas/abm_canchas.html", {"canchas":canchas}, {"precios":precios})
