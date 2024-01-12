from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from usuarios.forms import FormInicioSesion, FormNuevoCliente
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
        form = FormNuevoCliente()
        return render(request, "usuarios/registro.html", {"form": form})

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
