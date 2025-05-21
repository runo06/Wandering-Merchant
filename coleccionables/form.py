from django import forms
from .models import Coleccionable, UsuarioPersonalizado, Categoria
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class ColeccionableForm(forms.ModelForm):
    class Meta:
        model = Coleccionable
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen', 'stock']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'password1', 'password2']


class UsuarioForm(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'rol', 'password1', 'password2']

class UsuarioUpdateForm(UserChangeForm):
    password = None  # Ocultamos el campo contraseña
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'rol']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'imagen']