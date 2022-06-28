from rest_framework.viewsets import ModelViewSet

from .serializers import (
    ChatMsgSerializer,
    ChatSerializer,
    SpaceMsgSerializer,
    SpaceSerializer,
    StatusSerializer,
)

from .models import Chat, ChatMsg, Space, SpaceMsg, Status


# Space
class RoomModelViewSet(ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    # read_only_fields = ('account_name',)
    # write_only_fields = ('password',)  # Note: Password field is write-only


# RoomChat
class RoomMsgModelViewSet(ModelViewSet):
    queryset = SpaceMsg.objects.all()
    serializer_class = SpaceMsgSerializer


# Chat
class ChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ['updated', "created"]
    
    def get_queryset(self):
        # queryset =   Chat.objects.by_user(user=self.request.user).prefetch_related("chatmsg")
        # return queryset
        return Chat.objects.all()


# FriendChat
class ChatMsgModelViewSet(ModelViewSet):
    queryset = ChatMsg.objects.all()
    serializer_class = ChatMsgSerializer


# Status
class StatusModelViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer



    # def get_queryset(self):
    #     return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # def get_serializer_context(self):
    #     return {'product_id': self.kwargs['product_pk']}