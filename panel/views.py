from django.shortcuts import render, redirect, get_object_or_404
from coleccionables.models import Coleccionable, Categoria
from .form import ColeccionableForm, CategoriaForm
from django.contrib.auth.decorators import user_passes_test

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