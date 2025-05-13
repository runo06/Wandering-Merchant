from django import forms
from .models import Coleccionable

class ColeccionableForm(forms.ModelForm):
    class Meta:
        model = Coleccionable
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen', 'stock']
