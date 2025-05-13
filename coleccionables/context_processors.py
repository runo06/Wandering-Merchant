from .models import Categoria

def categorias_context(request):
    categorias = Categoria.objects.all()[:5]
    return {'categorias': categorias}
