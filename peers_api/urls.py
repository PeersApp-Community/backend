from django.urls import path
from rest_framework_nested import routers
from .views import (
    AllChatModelViewSet,
    AllSpaceModelViewSet,
    ChatMsgModelViewSet,
    ChatModelViewSet,
    ProfileModelViewSet,
    SpaceDelMsgModelViewSet,
    SpaceModelViewSet,
    SpaceMsgModelViewSet,
    UserInfo,
    ReplyModelViewSet,
    ThreadModelViewSet,
    ChatDelMsgModelViewSet,
    ArcSpaceModelViewSet,
    ArcChatModelViewSet,
)

from extras.views import (
    AllBooks,
    AllBooksRetrieveUpdateAPIView,
    BookListCreateAPIView,
    AllStoryModelViewSet,
    BookRetrieveUpdateDestroyAPIView,
    PrivBookListCreateAPIView,
    PrivBookRetrieveUpdateDestroyAPIView,
    SavedBookListCreateAPIView,
    SavedBookRetrieveUpdateAPIView,
    StoryModelViewSet,
    SpaceTaskModelViewSet,
    MyTaskModelViewSet,
    library,
)


# from base.models import Profile
# from base.views import ProfileViewSet


router = routers.DefaultRouter()

router.register("users", UserInfo, basename="users")
router.register("all-chats", AllChatModelViewSet, basename="chats")
router.register("all-spaces", AllSpaceModelViewSet)
router.register("all-stories", AllStoryModelViewSet)

# router.register("msg", ThreadModelViewSet)
# router.register("chat-msg", ChatMsgModelViewSet)


# Nested
spaces_router = routers.NestedDefaultRouter(router, "all-spaces", lookup="space")
spaces_router.register("tasks", ProfileModelViewSet, basename="space-task")


users_router = routers.NestedDefaultRouter(router, "users", lookup="user")
users_router.register("chats", ChatModelViewSet, basename="user-chats")
users_router.register("arc-chats", ArcChatModelViewSet, basename="user-arc-chats")
users_router.register("spaces", SpaceModelViewSet, basename="user-spaces")
users_router.register("arc-spaces", ArcSpaceModelViewSet, basename="user-arc-spaces")
users_router.register("profile", ProfileModelViewSet, basename="user-profile")
users_router.register("tasks", ProfileModelViewSet, basename="user-task")


# chats
chats_router = routers.NestedDefaultRouter(users_router, "chats", lookup="chat")
chats_router.register("msgs", ChatMsgModelViewSet, basename="chat-msgs")
chats_router.register("del-msgs", ChatDelMsgModelViewSet, basename="chat-del-msgs")


# Arc chats
arc_chats_router = routers.NestedDefaultRouter(users_router, "arc-chats", lookup="chat")
arc_chats_router.register("msgs", ChatMsgModelViewSet, basename="arc-chat-msgs")
arc_chats_router.register(
    "del-msgs", ChatDelMsgModelViewSet, basename="arc-chat-del-msgs"
)


# Space
space_router = routers.NestedDefaultRouter(users_router, "spaces", lookup="space")
space_router.register("msgs", SpaceMsgModelViewSet, basename="space-msgs")
space_router.register("del-msgs", SpaceDelMsgModelViewSet, basename="space-del-msgs")


# Arc Space
arc_space_router = routers.NestedDefaultRouter(
    users_router, "arc-spaces", lookup="space"
)
arc_space_router.register("msgs", SpaceMsgModelViewSet, basename="arc-space-msgs")
arc_space_router.register(
    "del-msgs", SpaceDelMsgModelViewSet, basename="arc-space-del-msgs"
)


# SpaceMsgs
spaceMsg_router = routers.NestedDefaultRouter(space_router, "msgs", lookup="msg")
spaceMsg_router.register("thread", ThreadModelViewSet, basename="msg-thread")


# Arc SpaceMsgs
arc_spaceMsg_router = routers.NestedDefaultRouter(
    arc_space_router, "msgs", lookup="msg"
)
arc_spaceMsg_router.register("thread", ThreadModelViewSet, basename="arc-msg-thread")


# Thread
thread_router = routers.NestedDefaultRouter(spaceMsg_router, "thread", lookup="thread")
thread_router.register("replies", ReplyModelViewSet, basename="reply")


# Profile
# profile_router = routers.NestedDefaultRouter(users_router, "profiles", lookup="profile")
# profile_router.register("posts", ChatMsgModelViewSet, basename="space-post")


urlpatterns = [
    path("books/", AllBooks.as_view()),
    path("books/<int:pk>/", AllBooksRetrieveUpdateAPIView.as_view()),
    path("users/<int:user_pk>/lib/", library),
    path("users/<int:user_pk>/lib/books/", BookListCreateAPIView.as_view()),
    path("users/<int:user_pk>/lib/saved/", SavedBookListCreateAPIView.as_view()),
    path("users/<int:user_pk>/lib/privbooks/", PrivBookListCreateAPIView.as_view()),
    path(
        "users/<int:user_pk>/lib/saved/<int:pk>/",
        SavedBookRetrieveUpdateAPIView.as_view(),
    ),
    path(
        "users/<int:user_pk>/lib/books/<int:pk>/",
        BookRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        "users/<int:user_pk>/lib/privbooks/<int:pk>/",
        PrivBookRetrieveUpdateDestroyAPIView.as_view(),
    ),
]


urlpatterns += (
    router.urls
    + users_router.urls
    + chats_router.urls
    + arc_space_router.urls
    + space_router.urls
    + spaceMsg_router.urls
    + thread_router.urls
    + arc_space_router.urls
    + arc_spaceMsg_router.urls
)
