from django import forms
from .models import Coleccionable, UsuarioPersonalizado, Categoria
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


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={**ESTILO_INPUT, 'placeholder': 'correo@ejemplo.com'})
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={**ESTILO_INPUT, 'placeholder': 'Nombre de usuario'}),
            'password1': forms.PasswordInput(attrs={**ESTILO_INPUT, 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={**ESTILO_INPUT, 'placeholder': 'Confirmar contraseña'}),
        }


class UsuarioForm(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'rol', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={**ESTILO_INPUT, 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={**ESTILO_INPUT, 'placeholder': 'Correo electrónico'}),
            'rol': forms.Select(attrs=ESTILO_SELECT),
            'password1': forms.PasswordInput(attrs={**ESTILO_INPUT, 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={**ESTILO_INPUT, 'placeholder': 'Confirmar contraseña'}),
        }


class UsuarioUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'rol']
        widgets = {
            'username': forms.TextInput(attrs=ESTILO_INPUT),
            'email': forms.EmailInput(attrs=ESTILO_INPUT),
            'rol': forms.Select(attrs=ESTILO_SELECT),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={**ESTILO_INPUT, 'placeholder': 'Nombre de la categoría'}),
            'imagen': forms.ClearableFileInput(attrs=ESTILO_FILE),
        }
