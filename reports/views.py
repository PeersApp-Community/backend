from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import Rating
from rest_framework import status
from base.models import Profile
from rest_framework.response import Response
from .serializers import DataSerializer, RatingSerializer
from peers_api.models import *


class RatingListAPIView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [
        AllowAny,
    ]


class DataListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = DataSerializer
    permission_classes = [
        AllowAny,
    ]
