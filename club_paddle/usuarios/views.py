from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from usuarios.forms import FormInicioSesion, FormModificarCliente, FormNuevoCliente
from usuarios.models import Cliente


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("menu_principal")

    if request.method == "POST":
        form = FormInicioSesion(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect("menu_principal")
    else:
        form = FormInicioSesion()
        return render(request, "usuarios/iniciar_sesion.html", {"form": form})


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("iniciar_sesion")


class VRegistro(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("menu_principal")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        mi_formulario = FormNuevoCliente()
        context = {
            "form": mi_formulario,
            "boton_submit": "Registrar",
            "titulo": "Registrarse",
            "descripcion": "Ingrese sus datos",
        }
        return render(request, "usuarios/registro.html", context)

    def post(self, request):
        form = FormNuevoCliente(request.POST)
        if form.is_valid():
            usuario = form.save()

            nuevo_cliente = Cliente(
                user=usuario,
                dni=form.cleaned_data["dni"],
                domicilio=form.cleaned_data["domicilio"],
                telefono=form.cleaned_data["telefono"],
            )

            nuevo_cliente.save()

            login(request, usuario)
            return redirect("menu_principal")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, "usuarios/registro.html", {"form": form})


@login_required
def menu_principal(request):
    if request.user.is_superuser:
        return render(request, "usuarios/menu_principal_admin.html")
    return render(request, "usuarios/menu_principal_cliente.html")


@login_required
def mi_cuenta(request):
    if request.method == "GET":
        return render(request, "usuarios/mi_cuenta.html")
    else:
        user_id = request.POST.get("confirmar")
        password = request.POST.get("password")
        user = User.objects.get(id=user_id)
        user_qs = User.objects.filter(id=user_id)
        contrasena_valida = check_password(password, user.password)
        if contrasena_valida:
            logout(request)
            user_qs.update(is_active=False)
            messages.success(request, "¡Cuenta desactivada con éxito!")
            return HttpResponseRedirect(reverse("iniciar_sesion"))
        else:
            messages.error(request, "La contraseña ingresada no es correcta")
            return HttpResponseRedirect(reverse("mi_cuenta"))


@login_required
def modificar_cuenta(request):
    if request.method == "GET":
        # obtener datos iniciales
        user = User.objects.get(id=request.user.id)
        cliente = Cliente.objects.get(user_id=request.user.id)
        datos_iniciales = {
            "first_name": user.first_name,
            "username": user.username,
            "last_name": user.last_name,
            "email": user.email,
            "dni": cliente.dni,
            "domicilio": cliente.domicilio,
            "telefono": cliente.telefono,
        }
        mi_formulario = FormModificarCliente(initial=datos_iniciales)
        context = {
            "form": mi_formulario,
            "boton_submit": "Modificar",
            "titulo": "Modificar Cuenta",
            "descripcion": "Modifique su cuenta",
        }
        return render(request, "usuarios/registro.html", context)
    else:
        mi_formulario = FormModificarCliente(request.POST, instance=request.user)
        if mi_formulario.is_valid():
            try:
                mi_formulario.save()

                datos_modificar_cliente = {
                    "dni": mi_formulario.cleaned_data["dni"],
                    "telefono": mi_formulario.cleaned_data["telefono"],
                    "domicilio": mi_formulario.cleaned_data["domicilio"],
                }
                cliente_qs = request.user.cliente
                cliente_qs.dni = datos_modificar_cliente["dni"]
                cliente_qs.telefono = datos_modificar_cliente["telefono"]
                cliente_qs.domicilio = datos_modificar_cliente["domicilio"]
                cliente_qs.save()

                messages.success(request, "¡Cuenta modificada con éxito!")
                return redirect("mi_cuenta")
            except Exception as e:
                messages.error(request, f"Error al modificar la cuenta: {str(e)}")
                context = {
                    "form": mi_formulario,
                    "boton_submit": "Modificar",
                    "titulo": "Modificar Cuenta",
                    "descripcion": "Modifique su cuenta",
                }
                return render(request, "usuarios/registro.html", context)
        else:
            # for msg in mi_formulario.error_messages:
            #    messages.error(request, mi_formulario.error_messages[msg])
            context = {
                "form": mi_formulario,
                "boton_submit": "Modificar",
                "titulo": "Modificar Cuenta",
                "descripcion": "Modifique su cuenta",
            }
            return render(request, "usuarios/registro.html", context)
