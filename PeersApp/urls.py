from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

admin.site.site_header = "PeersApp Admin"
admin.site.index_title = "Admin"


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("peers-admin/", admin.site.urls),
    path("api/", include("peers_api.urls")),
    path("base/", include("base.urls")),
    #
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("docs/", include_docs_urls(title="PeersApp API")),
    path(
        "api/schema/",
        get_schema_view(
            title="PeersApp", description="API for the PeersApp", version="1.0.0"
        ),
        name="PeersApp-schema",
    ),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
