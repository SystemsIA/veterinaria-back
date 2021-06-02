# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Rest
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # path("users/", include("veterinaria_back.users.urls", namespace="users")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
]
if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    # Include Docs too, and token with DRF
    urlpatterns += [
        # Django Allauth
        # path("accounts/", include("allauth.urls")),
        # DRF auth token
        path("auth-token/", obtain_auth_token),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Site
admin.site.site_header = "Administrador de VETERINARIA_BACK"
admin.site.site_title = "VETERINARIA_BACK"
admin.site.index_title = "Bienvenido al administrador de VETERINARIA_BACK"
