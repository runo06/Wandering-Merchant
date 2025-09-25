from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home , name='home'),
    path('home/', views.home, name='home'),
    path('busqueda/', views.busqueda, name='busqueda'),
    path('nosotros/', views.nosotros, name='nosotros'),  
    path('contactos/', views.contactos, name='contactos'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
]