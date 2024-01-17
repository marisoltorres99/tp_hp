from clases.models import Clase
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from usuarios.models import Cliente

from inscripciones.models import Inscripcion


def nueva_inscripcion(request):
    if request.method == "POST":
        # obtengo cliente
        cliente = Cliente.objects.get(user_id=request.user.id)

        # obtengo clase
        clase_id = request.POST.get("confirmar")
        clase = Clase.objects.get(clase_id=clase_id)

        # creo nueva inscripcion
        inscripcion = Inscripcion(
            cliente=cliente,
            clase=clase,
        )
        inscripcion.save()

        messages.success(request, "¡Su inscripción ha sido exitosa!")
        return HttpResponseRedirect(reverse("buscar_clases"))
