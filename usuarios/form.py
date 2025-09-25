from django import forms
from .models import UsuarioPersonalizado
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

class PerfilUsuarioForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ['first_name','username', 'last_name', 'email', 'telefono', 'biografia']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
                'placeholder': 'Ingresa tu nombre'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
                'disabled': 'disabled'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
                'placeholder': 'Ingresa tu apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
                'placeholder': 'Tu número de teléfono'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control bg-light text-dark border-0 shadow-sm rounded-3',
                'placeholder': 'Escribe tu biografía'
            }),
        }
