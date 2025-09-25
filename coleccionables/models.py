from django.db import models
from django.utils.text import slugify
from usuarios.models import UsuarioPersonalizado

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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='coleccionable')
    imagen = models.ImageField(upload_to='coleccionables/img/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='coleccionables')

    def __str__(self):
        return self.titulo
