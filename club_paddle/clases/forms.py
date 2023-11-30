from canchas.models import Cancha
from django import forms
from profesores.models import Profesor


class FormNuevaClase(forms.Form):
    cupo = forms.IntegerField(label="Cupo")
    cupo.widget.attrs.update({"class": "form-control"})
    cupo.widget.attrs.update({"placeholder": "ingrese cupo de la clase"})

    descripcion = forms.CharField(label="Descripcion")
    descripcion.widget.attrs.update({"class": "form-control"})
    descripcion.widget.attrs.update({"placeholder": "ingrese descripcion de la clase"})

    profesor = forms.ModelChoiceField(
        queryset=Profesor.objects.all(), empty_label="Seleccione un profesor"
    )

    cancha = forms.ModelChoiceField(
        queryset=Cancha.objects.all(), empty_label="Seleccione una cancha"
    )
