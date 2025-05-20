from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('usuario', 'Usuario'),
        ('vendedor', 'Vendedor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True) 
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Coleccionable(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='coleccionables/img/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='coleccionables')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='coleccionable')

    def __str__(self):
        return self.titulo


class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coleccionable = models.ForeignKey(Coleccionable, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Coleccionable, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)