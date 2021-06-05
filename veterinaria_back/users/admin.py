# Django
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Models
from veterinaria_back.users.models import Notificacion

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["email", "nombre", "tipo_usuario", "username", "activo", "is_superuser"]
    list_display_links = ["email", "nombre"]
    list_filter = ["is_superuser", "tipo_usuario"]
    # search_fields = []

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("email", "nombre", "tipo_usuario", "dni", ("direccion", "telefono"), "activo")},
        ),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (("is_active",), ("is_staff",), ("is_superuser",), ("groups"), ("user_permissions")),
            },
        ),
        (_("Important dates"), {"classes": ("collapse",), "fields": ("last_login", "date_joined")}),
        (_("Creación y actualización"), {"classes": ("collapse",), "fields": ("created", "modified")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "tipo_usuario", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("last_login", "date_joined", "created", "modified")


@admin.register(Notificacion)
class NotificaionAdmin(admin.ModelAdmin):
    list_display = ["cliente", "motivo", "visto"]
    list_filter = ["visto"]
    readonly_fields = ["created", "modified"]
