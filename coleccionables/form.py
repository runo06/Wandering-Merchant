from django import forms
from .models import Coleccionable
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UsuarioPersonalizado

class ColeccionableForm(forms.ModelForm):
    class Meta:
        model = Coleccionable
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen', 'stock']


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'rol', 'password1', 'password2']