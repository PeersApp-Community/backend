from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileRetrieveAPIView,
    ProfileUpdateAPIView,
    validate_user,
)

# Routers provide an easy way of automatically determining the URL conf.
#
urlpatterns = [
    path("validate/", validate_user),
    path("profile/", ProfileListAPIView.as_view()),
    path("profile/<int:pk>/", ProfileRetrieveAPIView.as_view()),
    path("profile/<int:id>/update/", ProfileUpdateAPIView.as_view()),
]
