from django.forms import ValidationError
from rest_framework import serializers
from base.models import Profile, User
from .models import Chat, ChatMsg, Space, SpaceMsg
from django.db.models import Q


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


# Room
class SpaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = [
            "id",
            "name",
            "host",
            "description",
            "participants",
        ]


# RoomChat
class SpaceMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceMsg
        fields = ["id", "author", "room", "message"]


# FriendChat
class ChatSerializer(serializers.ModelSerializer):
    user1 = UserSimpleSerializer()
    user2 = UserSimpleSerializer()

    class Meta:
        model = Chat
        fields = ["id", "user1", "user2", "updated", "created", "archived"]
        depth = 3


class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "user2"]

    def create(self, validated_data):
        user1_id = self.context.get("user1_id")
        return Chat.objects.create(user1_id=user1_id, **validated_data)

    def validate(self, attrs):
        user1 = self.context.get("user1_id")
        user2 = attrs["user2"]
        # lookup1 = Q(user1=user1) | Q(user2=user)
        lookup1 = Q(user1=user1) & Q(user2=user2)
        lookup2 = Q(user1=user2) & Q(user2=user1)

        if Chat.objects.filter(lookup1 | lookup2):
            raise ValidationError("Chat already exist")

        if int(user1) == int(user2.id):
            raise ValidationError("the second user is same as first user")

        return super().validate(attrs)


# ChatMsg
class ChatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMsg
        fields = [
            "id",
            "file",
            "message",
            "created",
            "updated",
            "seen",
            "pinned",
            "stared",
            "deleted",
            "retrieved",
        ]
        # fields = "__all__"
        # read_only_fields = ('account_name',)
        # write_only_fields = ('password',)  # Note: Password field is write-only

    def create(self, validated_data):
        chat_id = self.context.get("chat_id")
        user_id = self.context.get("user_id")
        return ChatMsg.objects.create(
            chat_id=chat_id, user_id=user_id, **validated_data
        )


class ProfileInlineSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Profile
        fields = "__all__"
        fields = [
            "id",
            "user_id",
            "user",
            "full_name",
            "bio",
            "gender",
            "institution",
            "educational_level",
            "course",
            "location",
            "updated",
            "avatar",
        ]

    # def save(self, **kwargs):
    #     # first_name = self.validated_data["first_name"]
    #     # last_name = self.validated_data["last_name"]

    #     try:
    #         user = User.objects.get(id=self.context["user_id"])
    #         user.save()
    #         return super().save(**kwargs)
    #     except:
    #         raise ValueError("error")
