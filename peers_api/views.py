from rest_framework.viewsets import ModelViewSet

from .serializers import (
    FriendChatSerializer,
    OrganisationSerializer,
    RoomChatSerializer,
    RoomSerializer,
    StatusSerializer,
)

from .models import FriendChat, Organisation, Room, RoomChat, Status


# Organisation
class OrganisationModelViewSet(ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


# Room
class RoomModelViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # read_only_fields = ('account_name',)
    # write_only_fields = ('password',)  # Note: Password field is write-only



# RoomChat
class RoomChatModelViewSet(ModelViewSet):
    queryset = RoomChat.objects.all()
    serializer_class = RoomChatSerializer


# FriendChat
class FriendChatModelViewSet(ModelViewSet):
    queryset = FriendChat.objects.all()
    serializer_class = FriendChatSerializer


# Status
class StatusModelViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
