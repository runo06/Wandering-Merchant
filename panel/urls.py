from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # CRUD productos
    path('coleccionables/ver/', views.lista_productos, name='lista_productos'),
    path('coleccionables/crear/', views.crear_coleccionable, name='crear_coleccionable'),
    path('coleccionables/editar/<int:pk>/', views.editar_coleccionable, name='editar_coleccionable'),
    path('coleccionables/eliminar/<int:pk>/', views.eliminar_coleccionable, name='eliminar_coleccionable'),

    # CRUD categorías
    path('categorias/ver/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


