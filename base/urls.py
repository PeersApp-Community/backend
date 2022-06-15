from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, UserCreateAPIView, validate_user
from django.urls import path

router = DefaultRouter()
# router.register("reg", UserCreateViewSet, basename="reg")
router.register("profile", ProfileViewSet)

# Routers provide an easy way of automatically determining the URL conf.
#
urlpatterns = [
    path("reg/", UserCreateAPIView.as_view()),
    path("reg/val/", validate_user),
]
urlpatterns += router.urls
