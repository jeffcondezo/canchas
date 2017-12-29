from django import forms


class AccesoForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)


class ReservaForm(forms.Form):
    idsucursal = forms.IntegerField()
    fecha = forms.DateField()
    tipocancha = forms.IntegerField()
    listahoras = forms.CharField(max_length=150)
