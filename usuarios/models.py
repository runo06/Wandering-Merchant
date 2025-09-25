from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('usuario', 'Usuario'),
        ('vendedor', 'Vendedor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'
