# Django
from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter

# Views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", ViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("rest-auth/", include("dj_rest_auth.urls")),
    # path("rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
