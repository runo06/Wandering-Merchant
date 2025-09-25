from django.shortcuts import render
from coleccionables.models import Coleccionable, Categoria

def contactos(request):
    return render(request, 'contactos.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def politica_privacidad(request):
    return render(request, 'politica_privacidad.html')

def terminos_condiciones(request):
    return render(request, 'terminos_condiciones.html')

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
