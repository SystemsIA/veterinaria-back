# Django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Rest
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # Ckeditor
    # url(r"^ckeditor/", include("ckeditor_uploader.urls")),
]


if settings.DEBUG:
    urlpatterns += [
        # DRF auth token
        path("auth-token/", obtain_auth_token)
    ]

# Site
admin.site.site_header = "Administrador de VETERINARIA_BACK"
admin.site.site_title = "VETERINARIA_BACK"
admin.site.index_title = "Bienvenido al administrador de VETERINARIA_BACK"
