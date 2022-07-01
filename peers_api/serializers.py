from rest_framework import serializers
from base.models import Profile, User
from .models import Chat, ChatMsg, Space, SpaceMsg


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "username"]


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


class ProfileInlineSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Profile
        fields = "__all__"
        # fields = [
        #     "id",
        #     "user_id",
        #     "user",
        #     "first_name",
        #     "last_name",
        #     "bio",
        #     "gender",
        #     "institution",
        #     "educational_level",
        #     "course",
        #     "location",
        #     "updated",
        #     "avatar",
        # ]
        
        
    def save(self, **kwargs):
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]

        print(kwargs)
        print(self.context)
        print("=================================")
        try:
            user = User.objects.get(id=self.context["user_id"])
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print("==============PROFILE=UPDATED==================")
            return super().save(**kwargs)
        except:
            print("=============PROFILE=ERROR===================")
            raise ValueError("error")
