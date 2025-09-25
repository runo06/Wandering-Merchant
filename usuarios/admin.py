from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado

class UsuarioPersonalizadoAdmin(UserAdmin):
    model = UsuarioPersonalizado
    list_display = ['username', 'email', 'rol', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Rol Personalizado', {'fields': ('rol',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol Personalizado', {'fields': ('rol',)}),
    )

admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)