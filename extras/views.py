from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.decorators import api_view
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from .models import MyTask, Story, Library, Book, SpaceTask, MyTask
from django.contrib.auth import get_user_model
from .serializers import (
    AllStorySerializer,
    BookSerializer,
    LibrarySerializer,
    MyTaskSerializer,
    SavedBookSerializer,
    SpaceTaskSerializer,
    StorySerializer,
)

User = get_user_model()

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


# Book
class AllBookModelViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.filter(public=True)
    http_method_names = ["get"]


# Book
class BookModelViewSet(ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(
            id__in=Library.objects.filter(
                id=self.kwargs.get("user_pk")
            ).prefetch_related("books"),
            public=True,
        )

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


# Library
# class LibraryModelViewSet(ModelViewSet):
#     serializer_class = LibrarySerializer
#     http_method_names = [
#         "get",
#         "put",
#         "patch",
#         "delete",
#         "head",
#         "options",
#     ]

#     def get_queryset(self):
#         return Library.objects.filter(id=self.kwargs.get("user_pk")).prefetch_related(
#             "books"
#         )

#     def get_serializer_context(self):
#         return {"user_id": self.kwargs.get("user_pk")}


# class BookPriModelViewSet(ModelViewSet):
#     serializer_class = BookSerializer

#     def get_queryset(self):
#         return Book.objects.filter(
#             id__in=Library.objects.filter(
#                 id=self.kwargs.get("user_pk")
#             ).prefetch_related("books"),
#             public=False,
#         )

#     def get_serializer_context(self):
#         return {"user_id": self.kwargs.get("user_pk")}


# Book
class PrivBookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(public=False, creator_id=self.kwargs.get("user_pk"))
        # .select_related("creator"),

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


class BookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(public=True, creator_id=self.kwargs.get("user_pk"))

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


class SavedBookListCreateAPIView(ListCreateAPIView):
    serializer_class = SavedBookSerializer
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        return (
            # User.objects.prefetch_related("saved_books")
            # .filter(id=self.kwargs.get("user_pk"))[0]
            # .saved_books.select_related("creator")
            # .prefetch_related("saved")
            Book.objects.exclude(creator_id=self.kwargs.get("user_pk"))
            .filter(public=True, saved__in=[self.kwargs.get("user_pk")])
            .select_related("creator")
            .prefetch_related("saved")
        )

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


class SavedBookRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = BookSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return (
            Book.objects.filter(public=True, id=self.kwargs.get("pk"))
            .select_related("creator")
            .prefetch_related("saved")
        )

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


class PrivBookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(
            public=False, id=self.kwargs.get("pk")
        ).prefetch_related("saved")

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(
            public=True, id=self.kwargs.get("pk")
        ).prefetch_related("saved")

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


@api_view(["PUT", "GET"])
def library(req, user_pk):
    if req.method == "GET":
        queryset = Library.objects.filter(id=user_pk).prefetch_related("books")
        serializer = LibrarySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllBooks(ListAPIView):
    serializer_class = SavedBookSerializer

    def get_queryset(self):
        return (
            Book.objects.filter(public=True)
            .prefetch_related("saved")
            .select_related("creator")
        )

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}
