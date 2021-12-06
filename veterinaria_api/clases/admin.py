# Django
from django.contrib import admin

# Models
from veterinaria_api.clases.models import (
    Cita,
    Especie,
    Estado,
    Historial,
    ImagenProducto,
    MarcaProducto,
    Mascota,
    Producto,
)
from veterinaria_api.users.models import User


# Producto
@admin.register(MarcaProducto)
class MarcaProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    readonly_fields = ["created", "modified"]


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]
    list_display = ["nombre", "precio", "stock"]
    search_fields = ["nombre", "marca__nombre"]
    list_filter = ["marca__nombre"]
    readonly_fields = ["created", "modified"]


# Mascota
@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ["tipo"]
    readonly_fields = ["created", "modified"]


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ["duenio", "nombre", "especie", "sexo"]
    search_fields = ["duenio__nombre", "nombre"]
    list_filter = ["sexo", "especie"]
    readonly_fields = ["created", "modified"]


# Historial
class EstadoInline(admin.TabularInline):
    model = Estado
    extra = 1


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    inlines = [EstadoInline]
    list_display = ["mascota", "tarea"]
    search_fields = ["mascota__nombre", "mascota__duenio__nombre", "medico__nombre"]
    list_filter = ["tarea", "internado"]
    readonly_fields = ["created", "modified"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "medico":
            try:
                kwargs["queryset"] = User.objects.filter(tipo_usuario=User.MEDICO)
            except Exception:
                pass
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# Cita
@admin.register(Cita)
class CitalAdmin(admin.ModelAdmin):
    list_display = ["cliente", "fecha_cita", "atendida", "cancelada"]
    search_fields = ["cliente__nombre"]
    list_filter = ["atendida", "cancelada"]
    readonly_fields = ["created", "modified"]
