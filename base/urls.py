from django.urls import path
from .loginSerializer import my_token_obtain_pair
from .views import (
    ProfileListAPIView,
    ProfileRetrieveAPIView,
    ProfileUpdateAPIView,
    login_view,
    refresh_OTP_view,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# Routers provide an easy way of automatically determining the URL conf.
#
urlpatterns = [
    path("validate/", my_token_obtain_pair),
    path("validate/refresh/", TokenRefreshView.as_view()),
    path("profile/", ProfileListAPIView.as_view()),
    path("profile/<int:pk>/", ProfileRetrieveAPIView.as_view()),
    path("profile/<int:id>/update/", ProfileUpdateAPIView.as_view()),
    path("login/", login_view),
    path("resend-otp/", refresh_OTP_view),
]
