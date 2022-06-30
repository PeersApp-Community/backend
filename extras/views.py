from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Space, Story
from .serializers import (
    AllStorySerializer,
    StorySerializer
)


# Story
class StoryModelViewSet(ModelViewSet):
    serializer_class = StorySerializer

    def get_queryset(self):
        return Story.objects.filter(user_id=self.kwargs["person_pk"])

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("person_pk")}


# All Story
class AllStoryModelViewSet(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = AllStorySerializer
