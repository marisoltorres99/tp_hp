from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from profesores.forms import FormNuevoProfesor
from profesores.models import Profesor


def abm_profesores(request):
    if request.method == "GET":
        profesores = Profesor.objects.all()
        context = {"profesores": profesores}
        return render(request, "profesores/abm_profesores.html", context)
    else:
        if "desactivar" in request.POST:
            profesor_id = request.POST.get("desactivar")
            profesor_qs = Profesor.objects.filter(profesor_id=profesor_id)
            profesor_qs.update(activo=False)
            messages.success(request, "¡Profesor desactivado con éxito!")
        else:
            profesor_id = request.POST.get("activar")
            profesor_qs = Profesor.objects.filter(profesor_id=profesor_id)
            profesor_qs.update(activo=True)
            messages.success(request, "¡Profesor activado con éxito!")
        return HttpResponseRedirect(reverse("Profesores"))


def nuevo_profesor(request):
    if request.method == "GET":
        mi_formulario = FormNuevoProfesor()
        context = {
            "form": mi_formulario,
            "boton_submit": "Cargar",
            "abm": "Nuevo Profesor",
        }
        return render(request, "profesores/form_profesor.html", context)
    else:
        mi_formulario = FormNuevoProfesor(request.POST)
        dni = request.POST.get("dni")
        # verificar si ya existe un profesor con el mismo DNI
        if Profesor.objects.filter(dni=dni).exists():
            messages.warning(request, "Ya existe un profesor con el mismo DNI.")
            context = {
                "form": mi_formulario,
                "boton_submit": "Cargar",
                "abm": "Nuevo Profesor",
            }
            return render(request, "profesores/form_profesor.html", context)
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
        return HttpResponseRedirect(reverse("NuevoProfesor"))


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
        context = {
            "form": mi_formulario,
            "boton_submit": "Modificar",
            "abm": "Editar Profesor",
        }
        return render(request, "profesores/form_profesor.html", context)
    else:
        mi_formulario = FormNuevoProfesor(request.POST)
        dni = request.POST.get("dni")
        profe_id = kwargs["profesor_id"]
        # verificar si ya existe un profesor con el mismo DNI
        if Profesor.objects.exclude(pk=profe_id).filter(dni=dni).exists():
            messages.warning(request, "Ya existe un profesor con el mismo DNI.")
            context = {
                "form": mi_formulario,
                "boton_submit": "Modificar",
                "abm": "Editar Profesor",
            }
            return render(request, "profesores/form_profesor.html", context)
        if mi_formulario.is_valid():
            datos_modificar = {
                "dni": mi_formulario.cleaned_data["dni"],
                "nombre_apellido": mi_formulario.cleaned_data["nombre_apellido"],
                "telefono": mi_formulario.cleaned_data["telefono"],
                "email": mi_formulario.cleaned_data["email"],
                "domicilio": mi_formulario.cleaned_data["domicilio"],
            }
            profe_id = kwargs["profesor_id"]
            profesor_qs = Profesor.objects.filter(profesor_id=profe_id)
            profesor_qs.update(**datos_modificar)
            messages.success(request, "¡Profesor modificado con éxito!")
        url_destino = reverse("EditarProfesor", kwargs={"profesor_id": profe_id})
        return HttpResponseRedirect(url_destino)
