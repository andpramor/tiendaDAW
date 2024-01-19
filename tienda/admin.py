from django.contrib import admin
from .models import Usuario, Marca, Producto, Compra
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('vip','saldo',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('vip','saldo',)}),)

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Compra)