from django.shortcuts import render

from apps.canchas.models import Cancha


def listado_canchas(request):
    canchas = Cancha.objects.all()
    context = {"canchas": canchas}
    return render(request, "canchas/listado_canchas.html", context)
