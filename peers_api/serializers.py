from django.forms import ValidationError
from rest_framework import serializers
from base.models import Profile, User, Friend
from .models import Chat, ChatMsg, Reply, Space, SpaceMsg, SpaceThread
from django.db.models import Q


class ProfileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "bio",
            "gender",
            "institution",
            "educational_level",
            "course",
            "location",
            "avatar",
        ]


class UserInfoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone"]


class UserInfoSimpleSerializer2(serializers.ModelSerializer):
    profile = ProfileSerializer2()

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "profile"]


class SpaceSimpleSerializer(serializers.ModelSerializer):
    host = UserInfoSimpleSerializer()

    class Meta:
        model = Space
        fields = ["id", "name", "host", "created", "updated"]


# Room
class SpaceSerializer(serializers.ModelSerializer):
    host = UserInfoSimpleSerializer()
    participants = UserInfoSimpleSerializer(many=True)

    class Meta:
        model = Space
        fields = [
            "id",
            "name",
            "host",
            "description",
            "archived",
            "pinned",
            "updated",
            "created",
            "admins",
            "participants",
        ]


# Room
class SpaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = [
            "id",
            "name",
            "description",
            "archived",
            "pinned",
            "admins",
            "participants",
        ]

    # def create(self, validated_data):

    def create(self, validated_data):
        new_validated_data = validated_data.copy()
        user_id = self.context.get("user_id")
        admins = new_validated_data.pop("admins")
        participants = new_validated_data.pop("participants")
        space = Space.objects.create(host_id=user_id, **new_validated_data)

        space.admins.set(admins)
        space.participants.set(participants)
        space.admins.add(user_id)
        space.participants.add(user_id)

        for admin in admins:
            space.participants.add(admin)

        return space


# RoomChat
class SpaceMsgSerializer(serializers.ModelSerializer):
    sender = UserInfoSimpleSerializer2()

    class Meta:
        model = SpaceMsg
        fields = [
            "id",
            "space_id",
            "message",
            "file",
            "pinned",
            "deleted",
            "updated",
            "created",
            "seen",
            "stared",
            "sender",
        ]


class SpaceCreateMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceMsg
        fields = [
            "id",
            "message",
            "file",
            "pinned",
            "deleted",
            "updated",
            "created",
            "seen",
            "stared",
        ]

    def create(self, validated_data):
        sender_id = self.context.get("user_id")
        space_id = self.context.get("space_id")
        spaceMsg = SpaceMsg.objects.create(
            sender_id=sender_id, space_id=space_id, **validated_data
        )
        return spaceMsg


# FriendChat
class ChatSerializer(serializers.ModelSerializer):
    user1 = UserInfoSimpleSerializer()
    user2 = UserInfoSimpleSerializer()

    class Meta:
        model = Chat
        fields = [
            "id",
            "user1",
            "user2",
            "updated",
            "created",
            "archived",
            "pinned",
            "deleted",
            "retrieved",
        ]


class ChatPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["archived", "pinned", "deleted", "retrieved"]


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

    def save(self, **kwargs):
        user1 = self.context.get("user1_id")
        user2 = self.validated_data["user2"]

        try:
            friends = Friend.objects.get(id=user1)
            friends.friend_list.add(user2)
        except Friend.DoesNotExist:
            Friend.objects.create(user_id=User.objects.get(id=user1), id=user1)
            print("CREATED NEW FRIEND_LIST")

        return super().save(**kwargs)


# ChatMsg
class ChatMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMsg
        fields = [
            "id",
            "sender_id",
            "file",
            "message",
            "created",
            "updated",
            "seen",
            "pinned",
            "stared",
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
            chat_id=chat_id, sender_id=user_id, **validated_data
        )


class ChatMsgPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMsg
        fields = ["id", "pinned", "deleted"]


class ProfileInlineSerializer(serializers.ModelSerializer):
    user = UserInfoSimpleSerializer()

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


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceThread
        fields = ["id", "thread_message_id"]


class ReplySerializer(serializers.ModelSerializer):
    user = UserInfoSimpleSerializer2()

    class Meta:
        model = Reply
        fields = ["id", "message", "file", "user"]


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["id", "message", "file", "user"]

    def create(self, validated_data):
        thread_id = self.context.get("thread_id")
        thread = Reply.objects.create(thread_id=thread_id, **validated_data)
        return thread
