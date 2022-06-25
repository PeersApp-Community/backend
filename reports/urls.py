from .views import RatingListAPIView
from django.urls import path

urlpatterns = [
    path("ratings", RatingListAPIView.as_view()),
]
