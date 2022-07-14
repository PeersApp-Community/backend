from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from .models import MyTask, Story, Library, Book, Genre, SpaceTask, MyTask
from .serializers import (
    AllStorySerializer,
    BookSerializer,
    GenreSerializer,
    LibrarySerializer,
    MyTaskSerializer,
    SpaceTaskSerializer,
    StorySerializer,
)


# StoryModelViewSet
class StoryModelViewSet(ModelViewSet):
    serializer_class = StorySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return Story.objects.filter(user_id=self.kwargs["user_pk"])

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# FriendStoryModelViewSet
class FriendStoryModelViewSet(ModelViewSet):
    serializer_class = StorySerializer

    def get_queryset(self):
        return Story.objects.filter(user_id=self.kwargs["user_pk"])

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# All Story
class AllStoryModelViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    queryset = Story.objects.all()
    serializer_class = AllStorySerializer


# Library
class LibraryModelViewSet(ModelViewSet):
    serializer_class = LibrarySerializer

    def get_queryset(self):
        return Library.objects.filter(id=self.kwargs.get("user_pk")).prefetch_related(
            "books"
        )

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# Book
class BookModelViewSet(ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter()

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# MyTask
class MyTaskModelViewSet(ModelViewSet):
    serializer_class = MyTaskSerializer

    def get_queryset(self):
        return MyTask.objects.filter()

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# SpaceTask
class SpaceTaskModelViewSet(ModelViewSet):
    serializer_class = SpaceTaskSerializer

    def get_queryset(self):
        return SpaceTask.objects.filter()

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# Genre
class GenreModelViewSet(ModelViewSet):
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.filter()

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}
