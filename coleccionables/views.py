from django.shortcuts import render, get_object_or_404
from .models import Coleccionable, Categoria



def lista_coleccionables(request):
    productos = Coleccionable.objects.all()
    return render(request, 'lista_coleccionables.html', {'productos': productos})

<<<<<<< Updated upstream
=======
def contactos(request):
    return render(request, 'contactos.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def crear_coleccionable(request):
    if request.method == 'POST':
        form = ColeccionableForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_coleccionables')  # Redirige a la lista después de guardar
    else:
        form = ColeccionableForm()
    
    return render(request, 'crear_coleccionable.html', {'form': form})

def home(request):
    productos_destacados = Coleccionable.objects.all()[:10]
    categorias = Categoria.objects.all()[:4]  
    return render(request, 'home.html', {'productos': productos_destacados, 'categorias': categorias})

def busqueda(request):
    query = request.GET.get('q')
    coleccionables = Coleccionable.objects.all()
    
    if query:
        coleccionables = coleccionables.filter(titulo__icontains=query)

    return render(request, 'busqueda.html', {
        'coleccionables': coleccionables,
        'query': query
    })

>>>>>>> Stashed changes
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
