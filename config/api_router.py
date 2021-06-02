# Django
from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter

# Views
from veterinaria_back.api.views import ProductoModelViewSet, UserChangePassword, DetailUser, MedicoModelViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("productos", ProductoModelViewSet, basename="productos")
router.register("medicos", MedicoModelViewSet, basename="medicos")

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("rest-auth/user/", DetailUser.as_view(), name="detail_user"),
    path("rest-auth/password/", UserChangePassword.as_view(), name="change_password"),
    path("rest-auth/", include("dj_rest_auth.urls"))
    # path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
