from rest_framework import serializers
from base.models import User
from .models import FriendChat, Organisation, Room, RoomChat, Status


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone"]


class OrganisationSimpleSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer()

    class Meta:
        model = Organisation
        fields = ["id", "name", "host", "created"]


class RoomSimpleSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer()

    class Meta:
        model = Room
        fields = ["id", "name", "host", "created", "updated"]


# Organisation
class OrganisationSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer()
    members = UserSimpleSerializer(many=True)

    class Meta:
        model = Organisation
        fields = ["id", "host", "name", "members", "created"]


# Room
class RoomSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer()

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "host",
            "description",
            "organisation",
            "created",
            "participants",
            "updated",
        ]


# RoomChat
class RoomChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomChat
        fields = ["id", "author", "room", "organisation", "body"]


# FriendChat
class FriendChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendChat
        fields = ["id", "sender", "receiver", "body"]


# Status
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "user", "post"]
