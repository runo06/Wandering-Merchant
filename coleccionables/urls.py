from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home , name='home'),
    path('home/', views.home, name='home'),
    path('busqueda/', views.busqueda, name='busqueda'),

    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'),

    
    path('registro/', views.registro, name='registro'),
    path('coleccionables/', views.lista_coleccionables, name='lista_coleccionables'),
    path('coleccionables/nuevo/', views.crear_coleccionable, name='crear_coleccionable'),

    path('nosotros/', views.nosotros, name='nosotros'),  
    path('contactos/', views.contactos, name='contactos'),  
    

    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/vendedor/', views.vendedor_dashboard, name='vendedor_dashboard'),
    
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),


    path('categoria/<slug:slug>/', views.productos_por_categoria, name='categoria'),

    path('categorias/', views.categorias, name='categorias'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('quitar-del-carrito/<int:producto_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('modificar-cantidad/<int:producto_id>/', views.modificar_cantidad, name='modificar_cantidad'),


    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),

    #CRUD
    path('coleccionables/ver/', views.lista_productos, name='lista_productos'),
    path('coleccionables/crear/', views.crear_coleccionable, name='crear_coleccionable'),
    path('coleccionables/editar/<int:pk>/', views.editar_coleccionable, name='editar_coleccionable'),
    path('coleccionables/eliminar/<int:pk>/', views.eliminar_coleccionable, name='eliminar_coleccionable'),

    #CRUD USUARIOS
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),

    #CRUD CATEGORIAS
    path('categorias/ver/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


