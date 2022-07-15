from rest_framework.response import Response

# from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import render
from uritemplate import partial

from base.serializers import (
    ProfileEditSerializer,
    ProfileImageSerializer,
    ProfileSerializer,
)

from .models import Chat, ChatMsg, Reply, Space, SpaceMsg, SpaceThread
from .serializers import (
    ChatCreateSerializer,
    ChatMsgSerializer,
    ChatPatchSerializer,
    ChatSerializer,
    ProfileInlineSerializer,
    ReplyCreateSerializer,
    ReplySerializer,
    SpaceCreateSerializer,
    SpaceMsgSerializer,
    SpaceSerializer,
    ThreadSerializer,
    UserInfoSimpleSerializer,
)
from base.models import Profile

User = get_user_model()


def testing(req):
    context = {}
    return render(req, "index.html", context)


class ProfileModelViewSet(ModelViewSet):
    serializer_class = ProfileInlineSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    http_method_names = ["get", "put", "patch", "head", "options"]

    def get_queryset(self):
        queryset = Profile.objects.filter(user_id=self.kwargs.get("user_pk"))
        return queryset

    def get_serializer_context(self):
        try:
            return {"user_id": self.kwargs["user_pk"]}
        except:
            pass

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return ProfileSerializer

            if self.request.method == "PUT":
                return ProfileEditSerializer
            # if self.request.method == "PATCH":
            #     return ProfileImageSerializer
        except:
            pass

        return ProfileEditSerializer

    @action(detail=True, methods=["PUT"])
    def upload(self, request, pk=None, *args, **kwargs):
        profile = Profile.objects.get(id=self.kwargs["user_pk"])
        serializer = ProfileImageSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSimpleSerializer
    http_method_names = ["get", "head", "options"]

    # permission_classes = [
    #     IsAuthenticated,
    # ]


# All Spaces
class AllSpaceModelViewSet(ModelViewSet):
    queryset = (
        Space.objects.filter(archived=False)
        .select_related("host")
        .prefetch_related("admins", "participants")
    )
    serializer_class = SpaceSerializer

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return SpaceSerializer
            return SpaceCreateSerializer
        except:
            pass

        return SpaceCreateSerializer


# Archived Spaces
class ArcSpaceModelViewSet(ModelViewSet):
    queryset = (
        Space.objects.filter(archived=True)
        .select_related("host")
        .prefetch_related("admins", "participants")
    )
    serializer_class = SpaceSerializer

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return SpaceSerializer
            return SpaceCreateSerializer
        except:
            pass

        return SpaceCreateSerializer


# Space
class SpaceModelViewSet(ModelViewSet):
    serializer_class = SpaceSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_pk")}

    def get_queryset(self):
        #    User.objects.get(id=self.kwargs.get("user_pk"))
        # .spaces.filter(archived=False)
        # .select_related("host")
        # .prefetch_related("participants", "admins")
        queryset = (
            Space.objects.filter(participants__in=[self.kwargs.get("user_pk")])
            .select_related("host")
            .prefetch_related("participants", "admins")
        )
        return queryset

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return SpaceSerializer
            return SpaceCreateSerializer
        except:
            pass

        return SpaceCreateSerializer

    @action(detail=False, methods=["GET"])
    def hosted(self, request, *args, **kwargs):
        hosted_spaces = Space.objects.filter(host_id=kwargs.get("user_pk"))
        serializer = SpaceSerializer(hosted_spaces, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def isadmin(self, request, *args, **kwargs):
        isadmin_spaces = (
            Space.objects.filter(
                admins__in=[
                    self.kwargs.get("user_pk"),
                ]
            )
            .select_related("host")
            .prefetch_related("admins", "participants")
        )
        serializer = SpaceSerializer(isadmin_spaces, many=True)
        return Response(serializer.data)


# SpaceMsgModelViewSet
class SpaceMsgModelViewSet(ModelViewSet):
    queryset = SpaceMsg.objects.all()
    serializer_class = SpaceMsgSerializer

    def get_queryset(self):
        queryset = SpaceMsg.objects.filter(
            space_id=self.kwargs.get("space_pk"), deleted=False
        ).select_related("sender__profile")
        return queryset

    def get_serializer_context(self):
        return {
            "space_id": self.kwargs.get("space_pk"),
            "user_id": self.kwargs.get("user_pk"),
        }


class SpaceDelMsgModelViewSet(ModelViewSet):
    queryset = SpaceMsg.objects.all()
    serializer_class = SpaceMsgSerializer

    def get_queryset(self):
        queryset = SpaceMsg.objects.filter(
            space_id=self.kwargs.get("space_pk"), deleted=True
        ).select_related("sender__profile")
        return queryset


# ArcChatModelViewSet
# Chat
class ArcChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ["updated", "created"]
    # http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        queryset = (
            Chat.objects.by_user(user=self.kwargs.get("user_pk"))
            .filter(archived=True, deleted=False)
            .select_related("user1", "user2")
        )
        return queryset


# Chat
class ChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ["updated", "created"]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        queryset = (
            Chat.objects.by_user(user=self.kwargs.get("user_pk"))
            .filter(archived=False, deleted=False)
            .select_related("user1", "user2")
        )
        return queryset

    def get_serializer_context(self):
        return {
            "user1_id": self.kwargs.get("user_pk"),
        }

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return ChatSerializer
            if self.request.method == "PATCH":
                return ChatPatchSerializer
            return ChatCreateSerializer
        except:
            pass

        return ChatCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        default_serializer = self.get_serializer(instance)
        current_user = self.kwargs.get("user_pk")
        serializer = default_serializer.data.copy()

        try:
            if int(serializer["user1"]["id"]) == int(current_user):
                serializer.pop("user2")
                serializer.pop("user1")
                other_user = default_serializer.data.pop("user2")

                second = {"other_user": other_user}

            else:
                other_user = default_serializer.data.pop("user1")
                serializer.pop("user1")
                serializer.pop("user2")

            second = {"other_user": other_user}

            second_user_profile = Profile.objects.filter(
                id=(second["other_user"]["id"])
            ).values(
                "full_name",
                "bio",
                "gender",
                "institution",
                "educational_level",
                "course",
                "location",
                "avatar",
            )
            second_user_new_profile = list(second_user_profile)[0]
            other_user.update(second_user_new_profile)
            serializer.update(second)

        except:
            print(f"Something is wrong with user {current_user}'s chat list")
            pass

        return Response(serializer)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        default_serializer = self.get_serializer(queryset, many=True)

        serializer = default_serializer.data.copy()

        current_user = self.kwargs.get("user_pk")

        try:
            profiles = Profile.objects.all()
            for item in serializer:
                if int(item["user1"]["id"]) == int(current_user):
                    other_user = item.pop("user2")
                    item.pop("user1")
                else:
                    other_user = item.pop("user1")
                    item.pop("user2")

                second = {"other_user": other_user}
                second_user_profile = profiles.filter(
                    id=(second["other_user"]["id"])
                ).values(
                    "full_name",
                    "bio",
                    "gender",
                    "institution",
                    "educational_level",
                    "course",
                    "location",
                    "avatar",
                )
                second_user_new_profile = list(second_user_profile)[0]
                other_user.update(second_user_new_profile)
                item.update(second)

        except:
            print(f"Something is wrong with {current_user}'s chat list")
            pass

        return Response(serializer)


# Chat
class AllChatModelViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    ordering_fields = ["updated", "created"]
    queryset = Chat.objects.all().select_related("user1", "user2")
    http_method_names = ["get", "head", "options"]


# FriendChatMsgs
class ChatMsgModelViewSet(ModelViewSet):
    serializer_class = ChatMsgSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        queryset = ChatMsg.objects.filter(
            chat_id=self.kwargs.get("chat_pk"), deleted=False
        )
        return queryset

    def get_serializer_context(self):
        return {
            "chat_id": self.kwargs.get("chat_pk"),
            "user_id": self.kwargs.get("user_pk"),
        }


class ChatDelMsgModelViewSet(ModelViewSet):
    serializer_class = ChatMsgSerializer

    def get_queryset(self):
        queryset = ChatMsg.objects.filter(
            chat_id=self.kwargs.get("chat_pk"), deleted=True
        )
        return queryset


# class ChatDelMsgMixins(
#     ListAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
# ):
#     serializer_class = ChatMsgSerializer
#
#
#     def get_queryset(self):
#         print(self.kwargs)
#         queryset = ChatMsg.objects.filter(
#             chat_id=self.kwargs.get("chat_pk"), deleted=True
#         )
#         return queryset


# ThreadModelViewSet
class ThreadModelViewSet(ModelViewSet):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        queryset = SpaceThread.objects.filter(id=self.kwargs.get("msg_pk"))
        return queryset


# ReplyModelViewSet
class ReplyModelViewSet(ModelViewSet):
    serializer_class = ReplySerializer

    def get_queryset(self):
        print(self.kwargs)
        queryset = Reply.objects.filter(
            thread_id=self.kwargs.get("msg_pk")
        ).select_related("user__profile")
        return queryset

    def get_serializer_context(self):
        print(self.kwargs)
        return {
            "msg_id": self.kwargs.get("msg_pk"),
            "user_id": self.kwargs.get("user_pk"),
            "thread_id": self.kwargs.get("thread_pk"),
        }

    def get_serializer_class(self):
        try:
            if self.request.method == "GET":
                return ReplySerializer
            # if self.request.method == "PATCH":
            #     return ChatPatchSerializer
            # return ChatCreateSerializer
        except:
            pass

        return ReplyCreateSerializer
