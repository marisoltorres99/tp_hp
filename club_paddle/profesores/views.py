from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render

from profesores.forms import FormNuevoProfesor
from profesores.models import Profesor


def abm_profesores(request):
    profesores = Profesor.objects.all()
    if request.method == "POST":
        if "desactivar_profesor" in request.POST:
            profesor_id = request.POST.get("desactivar_profesor")
            profesor = Profesor.objects.get(profesor_id=profesor_id)
            profesor.activo = False
            profesor.save()
        else:
            profesor_id = request.POST.get("activar_profesor")
            profesor = Profesor.objects.get(profesor_id=profesor_id)
            profesor.activo = True
            profesor.save()
    return render(request, "profesores/abm_profesores.html", {"profesores": profesores})


def nuevo_profesor(request):
    if request.method == "POST":
        mi_formulario = FormNuevoProfesor(request.POST)
        if mi_formulario.is_valid():
            dni = mi_formulario.cleaned_data["dni"]
            nombre_apellido = mi_formulario.cleaned_data["nombre_apellido"]
            telefono = mi_formulario.cleaned_data["telefono"]
            email = mi_formulario.cleaned_data["email"]
            domicilio = mi_formulario.cleaned_data["domicilio"]

            profesor = Profesor(
                dni=dni,
                nombre_apellido=nombre_apellido,
                telefono=telefono,
                email=email,
                domicilio=domicilio,
            )
            profesor.save()
            messages.success(request, "¡Profesor cargado con éxito!")
            return HttpResponseRedirect("/profesores/nuevo/")
    else:
        mi_formulario = FormNuevoProfesor()
    return render(
        request,
        "profesores/nuevo_profesor.html",
        {"form": mi_formulario},
    )


def editar_profesor(request, **kwargs):
    if request.method == "GET":
        profesor = Profesor.objects.get(profesor_id=kwargs["profesor_id"])
    datos_iniciales = {
        "dni": profesor.dni,
        "nombre_apellido": profesor.nombre_apellido,
        "telefono": profesor.telefono,
        "email": profesor.email,
        "domicilio": profesor.domicilio,
    }
    mi_formulario = FormNuevoProfesor(initial=datos_iniciales)

    return render(
        request,
        "profesores/editar_profesor.html",
        {"form": mi_formulario},
    )
