from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from base.serializers import ProfileEditSerializer,  ProfileSerializer
from extras.serializers import StorySerializer

from .models import Chat, ChatMsg, Space, SpaceMsg
from .serializers import (
    ChatCreateSerializer,
    ChatMsgSerializer,
    ChatSerializer,
    ProfileInlineSerializer,
    SpaceCreateSerializer,
    SpaceMsgSerializer,
    SpaceSerializer,
    SpaceSimpleSerializer,
    UserInfoSimpleerializer,
)
from base.models import Profile

User = get_user_model()


class ProfileModelViewSet(ModelViewSet):
    serializer_class = ProfileInlineSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        queryset = Profile.objects.filter(user_id=self.kwargs.get("user_pk"))
        return queryset

    def get_serializer_context(self):
        try:
            return {"user_id": self.kwargs["user_pk"]}
        except:
            pass

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return ProfileSerializer
            
            if self.request.method == "PUT":
                return ProfileEditSerializer
            # if self.request.method == "PATCH":
            #     return ProfileImageSerializer
        except:
            pass

        return ProfileEditSerializer

    @action(
        detail=True,
        methods=[
            "put",
        ],
    )
    def upload(self, request, pk=None, *args, **kwargs):
        profile = Profile.objects.get(id=self.kwargs["user_pk"])
        serializer = ProfileImageSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSimpleerializer
    http_method_names = ["get", "head", "options"]

    # permission_classes = [
    #     IsAuthenticated,
    # ]


# All Spaces
class AllSpaceModelViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    # read_only_fields = ('account_name',)
    # write_only_fields = ('password',)  # Note: Password field is write-only

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return SpaceSerializer
            return SpaceCreateSerializer
        except:
            pass

        return SpaceCreateSerializer


# Space
class SpaceModelViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

    # @action(
    #     detail=False,
    #     methods=[
    #         "GET",
    #     ],
    #     permission_classes=[AllowAny],
    # )
    # def hosted(self, request, *args, **kwargs):
    #     hosted_spaces = User.objects.get(
    #         id=self.kwargs.get("user_pk")
    #     ).hosted_spaces.all()

    #     serializer = SpaceSerializer(hosted_spaces)
    #     return Response(serializer.data)

    def get_serializer_context(self):
        return {"user1_id": self.kwargs.get("user_pk")}

    def get_queryset(self):
        queryset = User.objects.get(id=self.kwargs.get("user_pk")).spaces.all()
        return queryset

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return SpaceSerializer
            return SpaceCreateSerializer
        except:
            pass

        return SpaceCreateSerializer


# SpaceChat
class SpaceMsgModelViewSet(ModelViewSet):
    queryset = SpaceMsg.objects.all()
    serializer_class = SpaceMsgSerializer


# Chat
class ChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ["updated", "created"]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        queryset = Chat.objects.by_user(user=self.kwargs.get("user_pk"))
        # .prefetch_related("chat_msgs")
        # queryset = Chat.objects.filter(
        #     Q(sender_id=self.kwargs.get("user_pk"))
        #     | Q(receiver_id=self.kwargs.get("user_pk"))
        # )
        return queryset

    def get_serializer_context(self):
        return {
            "user1_id": self.kwargs.get("user_pk"),
        }

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return ChatSerializer
            return ChatCreateSerializer
        except:
            pass

        return ChatCreateSerializer


# Chat
class AllChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ["updated", "created"]
    queryset = Chat.objects.all()


# FriendChatMsgs
class ChatMsgModelViewSet(ModelViewSet):
    queryset = ChatMsg.objects.all()
    serializer_class = ChatMsgSerializer

    def get_queryset(self):
        queryset = ChatMsg.objects.filter(chat_id=self.kwargs.get("chat_pk"))
        return queryset

    def get_serializer_context(self):
        return {
            "chat_id": self.kwargs.get("chat_pk"),
            "user_id": self.kwargs.get("user_pk"),
        }
