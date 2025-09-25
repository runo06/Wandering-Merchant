from django.shortcuts import render, get_object_or_404
from .models import Coleccionable, Categoria



def lista_coleccionables(request):
    productos = Coleccionable.objects.all()
    return render(request, 'lista_coleccionables.html', {'productos': productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(Coleccionable, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})


def productos_por_categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    productos = categoria.coleccionable.all()[:5]
    return render(request, 'categorias.html', {
        'categoria': categoria,
        'productos': productos,
    })

def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})
