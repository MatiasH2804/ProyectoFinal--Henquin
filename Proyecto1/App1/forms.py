from django import forms
from .models import Ingreso, Gasto, Avatar

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['cantidad', 'categoria']  # Campos permitidos en el formulario

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['cantidad', 'categoria', 'medio_pago']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']
