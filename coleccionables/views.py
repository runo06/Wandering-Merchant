from django.shortcuts import render, redirect, get_object_or_404
from .models import Coleccionable, Categoria, Carrito, ItemCarrito
from .form import ColeccionableForm 
from .form import RegistroUsuarioForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def lista_coleccionables(request):
    productos = Coleccionable.objects.all()
    return render(request, 'lista_coleccionables.html', {'productos': productos})

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

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Coleccionable, id=producto_id)
    usuario = request.user

    carrito_item, creado = Carrito.objects.get_or_create(usuario=usuario, coleccionable=producto)

    if not creado:
        carrito_item.cantidad += 1
        carrito_item.save()
    else:
        carrito_item.cantidad = 1
        carrito_item.save()

    messages.success(request, 'Producto agregado al carrito')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def ver_carrito(request):
    usuario = request.user
    carrito_items = Carrito.objects.filter(usuario=usuario)
    total = sum(item.coleccionable.precio * item.cantidad for item in carrito_items)
    
    for item in carrito_items:
        item.subtotal = item.coleccionable.precio * item.cantidad
    
    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })

def quitar_del_carrito(request, producto_id):
    producto = get_object_or_404(Coleccionable, id=producto_id)
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    if producto in carrito.coleccionable.all():
        carrito.coleccionable.remove(producto)
        messages.success(request, f'Producto "{producto.nombre}" eliminado del carrito.')
    else:
        messages.warning(request, 'El producto no estaba en el carrito.')
    
    return redirect('ver_carrito')

def vaciar_carrito(request):
    Carrito.objects.filter(usuario=request.user).delete()
    messages.success(request, "Tu carrito ha sido vaciado.")
    return redirect('ver_carrito')


def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if request.user.is_authenticated:
            return redirect('home')  


        if user is not None:
            django_login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html') 

def user_logout(request):
    django_logout(request)
    return redirect('home')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            django_login(request, user)
            if user.rol == 'admin':
                return redirect('admin_dashboard')
            elif user.rol == 'vendedor':
                return redirect('vendedor_dashboard')
            else:
                return redirect('home')
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login_admin.html")

@login_required
def admin_dashboard(request):
    if request.user.rol != 'admin':
        return redirect('login')
    return render(request, 'paneles/admin_dashboard.html')

@login_required
def vendedor_dashboard(request):
    if request.user.rol != 'vendedor':
        return redirect('login')
    return render(request, 'paneles/vendedor_dashboard.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario registrado con éxito!')
            return redirect('login')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

# SE DEFINEN LAS VISTAS DE LAS POLITICAS Y TERMINOS

def politica_privacidad(request):
    return render(request, 'politica_privacidad.html')

def terminos_condiciones(request):
    return render(request, 'terminos_condiciones.html')