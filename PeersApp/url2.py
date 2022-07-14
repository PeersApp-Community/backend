from .urls import *


if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
