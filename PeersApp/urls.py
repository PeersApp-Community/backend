from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


admin.site.site_header = "PeersApp Admin"
admin.site.index_title = "Administrator"


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("peers-admin/", admin.site.urls),
    path("api/", include("peers_api.urls")),
    path("base/", include("base.urls")),
    path("reports/", include("reports.urls")),
    #
    path("auth/", include("djoser.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("docs/", include_docs_urls(title="PeersApp API")),
    path(
        "schema/",
        get_schema_view(
            title="PeersApp", description="API for the PeersApp", version="1.0.0"
        ),
        name="PeersApp-schema",
    ),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
