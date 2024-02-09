from django import forms


class FormNuevoProfesor(forms.Form):
    dni = forms.CharField(label="DNI", max_length=8, min_length=8)
    dni.widget.attrs.update({"class": "form-control"})
    dni.widget.attrs.update({"placeholder": "ingrese DNI"})

    nombre_apellido = forms.CharField(label="Nombre y Apellido")
    nombre_apellido.widget.attrs.update({"class": "form-control"})
    nombre_apellido.widget.attrs.update({"placeholder": "ingrese Nombre y Apellido"})

    telefono = forms.CharField(label="Telefono")
    telefono.widget.attrs.update({"class": "form-control"})
    telefono.widget.attrs.update({"placeholder": "ingrese telefono"})

    email = forms.EmailField(label="Email")
    email.widget.attrs.update({"class": "form-control"})
    email.widget.attrs.update({"placeholder": "ingrese email"})

    domicilio = forms.CharField(label="Domicilio")
    domicilio.widget.attrs.update({"class": "form-control"})
    domicilio.widget.attrs.update({"placeholder": "ingrese domicilio"})
