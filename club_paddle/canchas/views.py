from django.shortcuts import render

from canchas.models import Cancha, CanchaPrecios


def abm_canchas(request):
    canchas=Cancha.objects.all()
    return render(request, "canchas/abm_canchas.html", {"canchas":canchas})
