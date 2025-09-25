from django.shortcuts import render, redirect, get_object_or_404
from .models import Coleccionable, Carrito, ItemCarrito
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Coleccionable, id=producto_id)
    usuario = request.user

    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)

    item, item_creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not item_creado:
        item.cantidad += 1
        item.save()

    messages.success(request, 'Producto agregado al carrito')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def ver_carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = ItemCarrito.objects.filter(carrito=carrito)
    except Carrito.DoesNotExist:
        items = []

    total = 0
    for item in items:
        item.subtotal = item.producto.precio * item.cantidad
        total += item.subtotal

    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
    })


@login_required
def quitar_del_carrito(request, producto_id):
    producto = get_object_or_404(Coleccionable, id=producto_id)

    try:
        carrito = Carrito.objects.get(usuario=request.user)
        item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
        item.delete()
        messages.success(request, f'Producto "{producto.titulo}" eliminado del carrito.')
    except (Carrito.DoesNotExist, ItemCarrito.DoesNotExist):
        messages.warning(request, 'El producto no estaba en el carrito.')

    return redirect('ver_carrito')

@login_required
def modificar_cantidad(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad < 1:
            cantidad = 1
        
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            item = ItemCarrito.objects.get(carrito=carrito, producto_id=producto_id)
            item.cantidad = cantidad
            item.save()
            messages.success(request, 'Cantidad actualizada correctamente.')
        except (Carrito.DoesNotExist, ItemCarrito.DoesNotExist):
            messages.error(request, 'No se encontró el producto en el carrito.')
    
    return redirect('ver_carrito')


@login_required
def vaciar_carrito(request):
    Carrito.objects.filter(usuario=request.user).delete()
    messages.success(request, "Tu carrito ha sido vaciado.")
    return redirect('ver_carrito')
