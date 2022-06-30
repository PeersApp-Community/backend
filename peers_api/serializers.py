from rest_framework import serializers
from base.models import User
from .models import Chat, ChatMsg, Space, SpaceMsg


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
        fields = ["id", "person1", "person1_id", "person2", "person2_id", "updated"]


class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "person2"]

    def create(self, validated_data):
        person1_id = self.context.get("person1_id")
        print(person1_id)
        print("chat created")
        return Chat.objects.create(person1_id=person1_id, **validated_data)


# ChatMsg
class ChatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMsg
        # fields = ["id", "user", "chat", "file","message", "created", "updated","seen", ]
        fields = "__all__"

    def create(self, validated_data):
        chat_id = self.context.get("chat_id")
        return ChatMsg.objects.create(chat_id=chat_id, **validated_data)
