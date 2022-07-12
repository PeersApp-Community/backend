from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)


from .models import Story
from .serializers import AllStorySerializer, StorySerializer


# Story
class StoryModelViewSet(ModelViewSet):
    serializer_class = StorySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return Story.objects.filter(user_id=self.kwargs["user_pk"])

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}


# Story
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


# ===========================================
# ===========================================
# ===========================================
# @action(
#     detail=False,
#     methods=[
#         "put",
#     ],
# )
# def upload(self, request, pk=None):
#     serializer = AllStorySerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @action(
#     detail=True,
#     methods=[
#         "put",
#     ],
# )
# def upload(self, request, pk=None):
#     story = Story.objects.get(id=pk)
#     serializer = StorySerializer(story, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
