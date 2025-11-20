from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin

from .models import TipoEspacio, Espacio, Reserva, PerfilUsuario

# Inline para PerfilUsuario en User
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'

# Extender UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Integrar ImportExportModelAdmin en todos tus modelos

@admin.register(TipoEspacio)
class TipoEspacioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['nombre', 'capacidad_minima', 'capacidad_maxima']
    search_fields = ['nombre']

@admin.register(Espacio)
class EspacioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'capacidad', 'ubicacion', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre', 'codigo', 'ubicacion']
    list_editable = ['activo']

@admin.register(Reserva)
class ReservaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['espacio', 'usuario', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'estado']
    list_filter = ['estado', 'fecha_reserva', 'espacio__tipo']
    search_fields = ['usuario__username', 'espacio__nombre', 'motivo']
    date_hierarchy = 'fecha_reserva'

    def save_model(self, request, obj, form, change):
        if obj.estado == 'CONFIRMADA' and not obj.confirmada_por:
            obj.confirmada_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user', 'rol', 'telefono', 'departamento', 'notificaciones_email']  # <-- Cambiado 'usuario' por 'user'
    list_filter = ['rol', 'departamento']
    search_fields = ['user__username', 'telefono', 'departamento']  # <-- Cambiado 'usuario__username' por 'user__username'
