from django.contrib import admin
from .models import Area, Estado, Equipo, Sede

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_equipos', 'direccion')
    search_fields = ('nombre', 'direccion')
    
    def total_equipos(self, obj):
        return obj.equipos.count()
    total_equipos.short_description = "Total Equipos"

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'numero_serie', 'marca', 'modelo', 'sede', 'area', 'estado', 'garantia_vigente', 'fecha_registro')
    search_fields = ('nombre', 'numero_serie', 'marca', 'modelo', 'proveedor', 'tipo')
    list_filter = ('estado', 'area', 'sede', 'marca', 'fecha_compra', 'tipo')
    readonly_fields = ('numero_serie', 'fecha_registro', 'garantia_vigente')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo', 'numero_serie', 'observacion')
        }),
        ('Información Comercial', {
            'fields': ('marca', 'modelo', 'precio', 'proveedor', 'fecha_compra', 'garantia_hasta')
        }),
        ('Ubicación y Estado', {
            'fields': ('sede', 'area', 'estado')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro', 'garantia_vigente'),
            'classes': ('collapse',)
        }),
    )
    
    def garantia_vigente(self, obj):
        if obj.garantia_vigente:
            return "✅ Vigente"
        elif obj.garantia_hasta:
            return "❌ Vencida"
        else:
            return "❓ No definida"
    garantia_vigente.short_description = "Garantía"

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_equipos', 'descripcion')
    search_fields = ('nombre',)
    
    def total_equipos(self, obj):
        return obj.equipos.count()
    total_equipos.short_description = "Total Equipos"

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_equipos', 'descripcion')
    search_fields = ('nombre',)
    
    def total_equipos(self, obj):
        return obj.equipos.count()
    total_equipos.short_description = "Total Equipos"
