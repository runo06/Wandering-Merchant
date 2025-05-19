from django.shortcuts import render, redirect, get_object_or_404
from .models import Coleccionable, Categoria
from .form import ColeccionableForm 
from .form import RegistroUsuarioForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UsuarioPersonalizado

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
