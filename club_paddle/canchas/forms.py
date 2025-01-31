from django import forms


class FormNuevaCancha(forms.Form):
    numero = forms.IntegerField(label="Numero")
    numero.widget.attrs.update({"class": "form-control"})
    numero.widget.attrs.update({"placeholder": "ingrese numero de la cancha"})

    precio = forms.IntegerField(label="Precio")
    precio.widget.attrs.update({"class": "form-control"})
    precio.widget.attrs.update({"placeholder": "ingrese precio de la cancha"})

    imagen = forms.ImageField(label="Imagen", required=False)
    imagen.widget.attrs.update({"class": "form-control"})
    imagen.widget.attrs.update({"placeholder": "ingrese imagen de la cancha"})


class FormEditarCancha(forms.Form):
    precio = forms.IntegerField(label="Precio")
    precio.widget.attrs.update({"class": "form-control"})
    precio.widget.attrs.update({"placeholder": "ingrese precio de la cancha"})

    imagen = forms.ImageField(label="Imagen", required=False)
    imagen.widget.attrs.update({"class": "form-control"})
    imagen.widget.attrs.update({"placeholder": "ingrese imagen de la cancha"})
