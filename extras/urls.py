from django.urls import path

from .views import library

# from rest_framework_nested import routers


urlpatterns = [
    path("api/users/<int:user_pk>/libry/", library),
    path(),
]
