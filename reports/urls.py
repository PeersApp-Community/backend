from .views import DataListAPIView, RatingListAPIView
from django.urls import path

urlpatterns = [
    path("ratings", RatingListAPIView.as_view()),
    path("info", DataListAPIView.as_view()),
]
