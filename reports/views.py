from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import Rating
from rest_framework import status
from rest_framework.response import Response
from .serializers import  RatingSerializer


class RatingListAPIView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]
