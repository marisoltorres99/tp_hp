from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from usuarios.forms import FormNuevoCliente
from usuarios.models import Cliente


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("menu_principal")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect("menu_principal")
    else:
        form = AuthenticationForm()
        return render(request, "usuarios/iniciar_sesion.html", {"form": form})


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
