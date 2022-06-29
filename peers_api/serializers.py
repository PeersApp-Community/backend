from rest_framework import serializers
from base.models import User
from .models import Chat, ChatMsg, Space, SpaceMsg, Status


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone"]


class UserInfoSimpleerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone"]


class SpaceSimpleSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer()

    class Meta:
        model = Space
        fields = ["id", "name", "host", "created", "updated"]


# Organisation


# Room
class SpaceSerializer(serializers.ModelSerializer):
    host = UserSimpleSerializer()
    participants = UserSimpleSerializer(many=True)

    class Meta:
        model = Space
        fields = [
            "id",
            "name",
            "host",
            "description",
            "created",
            "participants",
            "updated",
        ]


# RoomChat
class SpaceMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceMsg
        fields = ["id", "author", "room", "message"]


# FriendChat
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "person1", "person1_id", "person2","person2_id", "updated"]


# ChatMsg
class ChatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMsg
        fields = ["id", "user", "chat", "message", "updated"]

    def create(self, validated_data):
        chat_id = self.context["chat_id"]
        return ChatMsg.objects.create(chat_id=chat_id, **validated_data)


# Status
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "user", "file", "text", "seen", "created", "updated"]
