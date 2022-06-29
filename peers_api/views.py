from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Chat, ChatMsg, Space, SpaceMsg, Story
from .serializers import (
    ChatMsgSerializer,
    ChatSerializer,
    SpaceMsgSerializer,
    SpaceSerializer,
    StorySerializer,
    UserInfoSimpleerializer,
)

User = get_user_model()


class UserInfo(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSimpleerializer

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


# Space
class SpaceModelViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    # read_only_fields = ('account_name',)
    # write_only_fields = ('password',)  # Note: Password field is write-only


# RoomChat
class SpaceMsgModelViewSet(ModelViewSet):
    queryset = SpaceMsg.objects.all()
    serializer_class = SpaceMsgSerializer


# Chat
class ChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ["updated", "created"]
    # queryset= Chat.objects.all()

    def get_queryset(self):
        queryset = Chat.objects.by_user(user=self.kwargs.get("person_pk"))
        # .prefetch_related("chat_msgs")
        # queryset = Chat.objects.filter(
        #     Q(sender_id=self.kwargs.get("person_pk"))
        #     | Q(receiver_id=self.kwargs.get("person_pk"))
        # )
        return queryset


# FriendChat
class ChatMsgModelViewSet(ModelViewSet):
    queryset = ChatMsg.objects.all()
    serializer_class = ChatMsgSerializer

    def get_queryset(self):
        queryset = ChatMsg.objects.filter(chat_id=self.kwargs.get("chat_pk"))
        return queryset


# Story
class StoryModelViewSet(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    # def get_queryset(self):
    #     return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # def get_serializer_context(self):
    #     return {'product_id': self.kwargs['product_pk']}
