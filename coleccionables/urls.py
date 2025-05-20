from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home , name='home'),
    path('home/', views.home, name='home'),  
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

    path('categoria/<slug:slug>/', views.productos_por_categoria, name='categoria'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),

    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


