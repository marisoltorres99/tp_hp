from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
    UsernameField,
)

from .models import User


class FormNuevoCliente(UserCreationForm):
    # redefinir mensajes
    mensaje = "Por favor, complete este campo"
    oninvalid_js_action = f"this.setCustomValidity('{mensaje}')"
    oninput_js_action = "this.setCustomValidity('')"

    dni = forms.CharField(label="DNI", max_length=8)
    dni.widget.attrs.update({"class": "form-control"})
    dni.widget.attrs.update({"placeholder": "ingrese DNI"})
    dni.widget.attrs.update({"oninvalid": oninvalid_js_action})
    dni.widget.attrs.update({"oninput": oninput_js_action})

    domicilio = forms.CharField(label="Domicilio", max_length=20)
    domicilio.widget.attrs.update({"class": "form-control"})
    domicilio.widget.attrs.update({"placeholder": "ingrese domicilio"})
    domicilio.widget.attrs.update({"oninvalid": oninvalid_js_action})
    domicilio.widget.attrs.update({"oninput": oninput_js_action})

    telefono = forms.CharField(label="Telefono", max_length=20)
    telefono.widget.attrs.update({"class": "form-control"})
    telefono.widget.attrs.update({"placeholder": "ingrese telefono"})
    telefono.widget.attrs.update({"oninvalid": oninvalid_js_action})
    telefono.widget.attrs.update({"oninput": oninput_js_action})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField}

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese nombre de usuario",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese apellido",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese email",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # redefinir mensajes
        mensaje = "Por favor, complete este campo"
        oninvalid_js_action = f"this.setCustomValidity('{mensaje}')"
        oninput_js_action = "this.setCustomValidity('')"

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "ingrese contraseña"
        self.fields["password1"].widget.attrs["oninvalid"] = oninvalid_js_action
        self.fields["password1"].widget.attrs["oninput"] = oninput_js_action

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "ingrese contraseña nuevamente"
        self.fields["password2"].widget.attrs["oninvalid"] = oninvalid_js_action
        self.fields["password2"].widget.attrs["oninput"] = oninput_js_action


class FormInicioSesion(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # redefinir mensajes
        mensaje = "Por favor, complete este campo"
        oninvalid_js_action = f"this.setCustomValidity('{mensaje}')"
        oninput_js_action = "this.setCustomValidity('')"

        # agrego clases bootstrap
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["oninvalid"] = oninvalid_js_action
        self.fields["username"].widget.attrs["oninput"] = oninput_js_action

        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["oninvalid"] = oninvalid_js_action
        self.fields["password"].widget.attrs["oninput"] = oninput_js_action


class FormModificarCliente(UserChangeForm):
    dni = forms.CharField(label="DNI", max_length=8)
    dni.widget.attrs.update({"class": "form-control"})
    dni.widget.attrs.update({"placeholder": "ingrese DNI"})

    domicilio = forms.CharField(label="Domicilio", max_length=20)
    domicilio.widget.attrs.update({"class": "form-control"})
    domicilio.widget.attrs.update({"placeholder": "ingrese domicilio"})

    telefono = forms.CharField(label="Telefono", max_length=20)
    telefono.widget.attrs.update({"class": "form-control"})
    telefono.widget.attrs.update({"placeholder": "ingrese telefono"})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField}

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese nombre de usuario",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese apellido",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ingrese email",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
