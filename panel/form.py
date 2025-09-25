from django import forms
from coleccionables.models import Coleccionable, Categoria
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

ESTILO_INPUT = {
    'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
    'placeholder': 'Escribe aquí...'
}

ESTILO_SELECT = {
    'class': 'form-select bg-light text-dark border-0 shadow-sm rounded-3'
}

ESTILO_FILE = {
    'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3'
}

class ColeccionableForm(forms.ModelForm):
    class Meta:
        model = Coleccionable
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen', 'stock']
        widgets = {
            'titulo': forms.TextInput(attrs=ESTILO_INPUT),
            'descripcion': forms.Textarea(attrs={**ESTILO_INPUT, 'rows': 3}),
            'precio': forms.NumberInput(attrs=ESTILO_INPUT),
            'categoria': forms.Select(attrs=ESTILO_SELECT),
            'imagen': forms.ClearableFileInput(attrs=ESTILO_FILE),
            'stock': forms.NumberInput(attrs=ESTILO_INPUT),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={**ESTILO_INPUT, 'placeholder': 'Nombre de la categoría'}),
            'imagen': forms.ClearableFileInput(attrs=ESTILO_FILE),
        }
