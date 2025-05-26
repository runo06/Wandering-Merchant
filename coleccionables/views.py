from django.shortcuts import render, redirect, get_object_or_404
from .models import Coleccionable, Categoria, Carrito, ItemCarrito, UsuarioPersonalizado
from .form import ColeccionableForm, UsuarioForm, UsuarioUpdateForm, RegistroUsuarioForm, CategoriaForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,  user_passes_test


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

def busqueda(request):
    query = request.GET.get('q')
    coleccionables = Coleccionable.objects.all()
    
    if query:
        coleccionables = coleccionables.filter(titulo__icontains=query)

    return render(request, 'busqueda.html', {
        'coleccionables': coleccionables,
        'query': query
    })

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
            usuario = form.save(commit=False)
            usuario.rol = 'usuario'  
            usuario.save()
            return redirect('login')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

# SE DEFINEN LAS VISTAS DE LAS POLITICAS Y TERMINOS

def politica_privacidad(request):
    return render(request, 'politica_privacidad.html')

def terminos_condiciones(request):
    return render(request, 'terminos_condiciones.html')

# CRUD

def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'

@user_passes_test(es_admin)
def lista_productos(request):
    coleccionables = Coleccionable.objects.all()
    return render(request, 'coleccionables/lista.html', {'coleccionables': coleccionables})

@user_passes_test(es_admin)
def crear_coleccionable(request):
    if request.method == 'POST':
        form = ColeccionableForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.vendedor = request.user
            nuevo.save()
            return redirect('lista_productos')
    else:
        form = ColeccionableForm()
    return render(request, 'coleccionables/formulario.html', {'form': form, 'accion': 'Crear'})

@user_passes_test(es_admin)
def editar_coleccionable(request, pk):
    coleccionable = get_object_or_404(Coleccionable, pk=pk)
    if request.method == 'POST':
        form = ColeccionableForm(request.POST, request.FILES, instance=coleccionable)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ColeccionableForm(instance=coleccionable)
    return render(request, 'coleccionables/formulario.html', {'form': form, 'accion': 'Editar'})

@user_passes_test(es_admin)
def eliminar_coleccionable(request, pk):
    coleccionable = get_object_or_404(Coleccionable, pk=pk)
    if request.method == 'POST':
        coleccionable.delete()
        return redirect('lista_productos')
    return render(request, 'coleccionables/eliminar.html', {'coleccionable': coleccionable})

# CRUD USUARIOS
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = UsuarioPersonalizado.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/formulario.html', {'form': form, 'accion': 'Crear'})

@user_passes_test(es_admin)
def editar_usuario(request, pk):
    usuario = get_object_or_404(UsuarioPersonalizado, pk=pk)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'usuarios/formulario.html', {'form': form, 'accion': 'Editar'})

@user_passes_test(es_admin)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(UsuarioPersonalizado, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

#CRUD CATEGORIAS
@user_passes_test(es_admin)
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

@user_passes_test(es_admin)
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/formulario.html', {'form': form, 'accion': 'Crear'})

@user_passes_test(es_admin)
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/formulario.html', {'form': form, 'accion': 'Editar'})

@user_passes_test(es_admin)
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'categorias/eliminar.html', {'categoria': categoria})