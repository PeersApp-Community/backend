from rest_framework_nested import routers
from .views import (
    ChatMsgModelViewSet,
    ChatModelViewSet,
    ProfileModelViewSet,
    AllSpaceModelViewSet,
    SpaceModelViewSet,
    SpaceMsgModelViewSet,
    UserInfo,
)
from extras.views import AllStoryModelViewSet, StoryModelViewSet

# from base.models import Profile
# from base.views import ProfileViewSet


router = routers.DefaultRouter()


router.register("users", UserInfo, basename="users")
router.register("all-chats", ChatModelViewSet, basename="chats")
router.register("all-spaces", AllSpaceModelViewSet)
router.register("all-stories", AllStoryModelViewSet)
# router.register("room-msg", SpaceMsgModelViewSet)
# router.register("chat-msg", ChatMsgModelViewSet)


# Nested
spaces_router = routers.NestedDefaultRouter(router, "all-spaces", lookup="space")
spaces_router.register("tasks", ProfileModelViewSet, basename="space-task")
# spaces_router.register("library", ProfileModelViewSet, basename="space-library")


users_router = routers.NestedDefaultRouter(router, "users", lookup="user")
users_router.register("chats", ChatModelViewSet, basename="user-chats")
users_router.register("spaces", SpaceModelViewSet, basename="user-spaces")
users_router.register("stories", StoryModelViewSet, basename="user-story")
users_router.register("profile", ProfileModelViewSet, basename="user-profile")
users_router.register("library", ProfileModelViewSet, basename="user-library")
users_router.register("tasks", ProfileModelViewSet, basename="user-task")


# chats
chats_router = routers.NestedDefaultRouter(users_router, "chats", lookup="chat")
chats_router.register("msgs", ChatMsgModelViewSet, basename="chat-msgs")


# Space
space_router = routers.NestedDefaultRouter(users_router, "spaces", lookup="space")
space_router.register("msgs", SpaceMsgModelViewSet, basename="space-msgs")


# Profile
# profile_router = routers.NestedDefaultRouter(users_router, "profiles", lookup="profile")
# profile_router.register("posts", ChatMsgModelViewSet, basename="space-post")

urlpatterns = router.urls + users_router.urls + chats_router.urls + space_router.urls
