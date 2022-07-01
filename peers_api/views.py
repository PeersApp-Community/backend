# from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from base.serializers import ProfileEditSerializer, ProfileSerializer

from .models import Chat, ChatMsg, Space, SpaceMsg
from .serializers import (
    ChatCreateSerializer,
    ChatMsgSerializer,
    ChatSerializer,
    ProfileInlineSerializer,
    SpaceMsgSerializer,
    SpaceSerializer,
    UserInfoSimpleerializer,
)
from base.models import Profile

User = get_user_model()


class UserInfo(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSimpleerializer
    # permission_classes = [
    #     IsAuthenticated,
    # ]

    # @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    # def history(self, request, pk):
    #     return Response('ok')

    # def chats(self, request):
    # @action(
    #     detail=True,
    #     methods=["GET", "PUT", "POST"],
    #     permission_classes=[AllowAny],
    # )
    # def chat(self, *args, **kwargs):
    #     print("==============================================")
    #     print("==============================================")
    #     user = Chat.objects.filter(sender=self.request.user.id)
    #     serializer = ChatSerializer(user)
    #     print("==============================================")
    #     # serializer.is_valid(raise_exception=True)
    #     # serializer.save()
    #     return Response(serializer.data)

    # @action(
    #     detail=False,
    #     methods=["GET", "PUT", "POST"],
    #     permission_classes=[AllowAny],
    # )
    # def chats1(self):
    #     user_chat = Chat.objects.filter(sender_id=request.user.id)
    #     serializer = ChatSerializer(user_chat)
    #     # serializer.is_valid(raise_exception=True)
    #     # serializer.save()
    #     return Response(serializer.data)

    # @action(
    #     detail=True,
    #     methods=["GET", "PUT", "POST"],
    #     permission_classes=[AllowAny],
    # )

    # def chats2(self, request):
    #     user = User.objects.get(id=request.user.id)
    #     serializer = UserInfoSimpleerializer(user, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


# All Spaces
class SpaceModelViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    # read_only_fields = ('account_name',)
    # write_only_fields = ('password',)  # Note: Password field is write-only

    def get_serializer_context(self):
        return {"person1_id": self.kwargs.get("person_pk")}


# Space
class SpaceModelViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    # read_only_fields = ('account_name',)
    # write_only_fields = ('password',)  # Note: Password field is write-only

    def get_serializer_context(self):
        return {"person1_id": self.kwargs.get("person_pk")}

    def get_queryset(self):
        queryset = Space.objects.filter()
        return super().get_queryset()


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
        queryset = Chat.objects.by_user(user=self.kwargs.get("person_pk"))
        # .prefetch_related("chat_msgs")
        # queryset = Chat.objects.filter(
        #     Q(sender_id=self.kwargs.get("person_pk"))
        #     | Q(receiver_id=self.kwargs.get("person_pk"))
        # )
        return queryset

    def get_serializer_context(self):
        return {"person1_id": self.kwargs.get("person_pk")}

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
        return {"chat_id": self.kwargs.get("chat_pk")}


class ProfileModelViewSet(ModelViewSet):
    serializer_class = ProfileInlineSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch", "put", "head", "options"]

    def get_queryset(self):
        queryset = Profile.objects.filter(user_id=self.kwargs.get("person_pk"))
        return queryset

    def get_serializer_context(self):
        try:
            return {"user_id": self.kwargs["person_pk"]}
        except:
            pass

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return ProfileSerializer

        except:
            pass

        return ProfileEditSerializer
