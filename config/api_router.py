# Django
from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

# Views
from veterinaria_api.api.views import (
    CitaModelViewSet,
    ClienteModelViewSet,
    DetailUserApiView,
    EspecieModelViewSet,
    HistoriasModelViewSet,
    MascotaModelViewSet,
    MedicoModelViewSet,
    NotificacionUserApiView,
    ProductoModelViewSet,
    UserChangePassword,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("productos", ProductoModelViewSet, basename="productos")
router.register("clientes", ClienteModelViewSet, basename="clientes")
router.register("mascotas", MascotaModelViewSet, basename="mascotas")
router.register("medicos", MedicoModelViewSet, basename="medicos")
router.register("especies", EspecieModelViewSet, basename="especies")
router.register("historias", HistoriasModelViewSet, basename="historias")
router.register("citas", CitaModelViewSet, basename="citas")

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("rest-auth/user/", DetailUserApiView.as_view(), name="detail_user"),
    path(
        "rest-auth/user/notificaciones/",
        NotificacionUserApiView.as_view(),
        name="notification_user",
    ),
    path("rest-auth/password/", UserChangePassword.as_view(), name="change_password"),
    path("rest-auth/", include("dj_rest_auth.urls"))
    # path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
