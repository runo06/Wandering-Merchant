from django.shortcuts import render, redirect, get_object_or_404
from .models import UsuarioPersonalizado
from .form import UsuarioForm, UsuarioUpdateForm, RegistroUsuarioForm, PerfilUsuarioForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,  user_passes_test

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

@login_required
def perfil(request):
    usuario = request.user  

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil') 
    else:
        form = PerfilUsuarioForm(instance=usuario)

    return render(request, 'perfil.html', {
        'form': form,
        'usuario': usuario 
    })

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


def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'
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