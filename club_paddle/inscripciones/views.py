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

        # busco inscripciones del cliente
        cliente = Cliente.objects.get(user_id=request.user.id)
        inscripciones_cliente_qs = Inscripcion.objects.filter(cliente=cliente)

        # Variable para verificar si el cliente ya está inscrito
        ya_inscrito = False

        for inscripcion in inscripciones_cliente_qs:
            if inscripcion.clase == clase:
                # El cliente ya está inscrito
                ya_inscrito = True
                break

        if not ya_inscrito:
            # Crear nueva inscripción
            nueva_inscripcion = Inscripcion(
                cliente=cliente,
                clase=clase,
            )
            nueva_inscripcion.save()
            messages.success(request, "¡Su inscripción ha sido exitosa!")
            return HttpResponseRedirect(reverse("buscar_clases"), {"alerta": "success"})
        else:
            messages.warning(request, "Usted ya está inscrito a esta clase.")
            return HttpResponseRedirect(reverse("buscar_clases"), {"alerta": "warning"})
