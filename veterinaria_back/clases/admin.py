# Django
from django.contrib import admin

# Models
from veterinaria_back.clases.models import (
    Cita,
    Estado,
    Historial,
    MarcaProducto,
    Producto,
    ImagenProducto,
    Mascota,
    Vacuna,
    DetalleVacuna,
)
from veterinaria_back.users.models import User


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
class DetalleVacunaInline(admin.TabularInline):
    model = DetalleVacuna
    extra = 1
    readonly_fields = ["created"]


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "enfermedad"]
    readonly_fields = ["created", "modified"]


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    inlines = [DetalleVacunaInline]
    list_display = ["duenio", "nombre", "sexo"]
    search_fields = ["duenio__nombre", "nombre"]
    list_filter = ["sexo"]
    readonly_fields = ["created", "modified"]


# Historial
class EstadoInline(admin.TabularInline):
    model = Estado
    extra = 1


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    inlines = [EstadoInline]
    list_display = ["mascota"]
    search_fields = ["mascota__nombre", "mascota__duenio__nombre", "medico__nombre"]
    list_filter = ["cirugia"]
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
