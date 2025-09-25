from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< Updated upstream
=======
    path('', views.home , name='home'),
    path('home/', views.home, name='home'),
    path('busqueda/', views.busqueda, name='busqueda'),  
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'),
    path('registro/', views.registro, name='registro'),
>>>>>>> Stashed changes
    path('coleccionables/', views.lista_coleccionables, name='lista_coleccionables'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('categoria/<slug:slug>/', views.productos_por_categoria, name='categoria'),
    path('categorias/', views.categorias, name='categorias'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


