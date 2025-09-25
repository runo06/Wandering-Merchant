from coleccionables.models import Categoria
from carrito.models import Carrito, ItemCarrito

def categorias_context(request):
    categorias = Categoria.objects.all()[:5]
    return {'categorias': categorias}

def cart_count(request):
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            count = ItemCarrito.objects.filter(carrito=carrito).count()
        except Carrito.DoesNotExist:
            count = 0
    else:
        count = 0
    return {'cart_count': count}