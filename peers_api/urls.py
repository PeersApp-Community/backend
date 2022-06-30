from rest_framework_nested import routers
from .views import (
    ChatMsgModelViewSet,
    ChatModelViewSet,
    SpaceModelViewSet,
    SpaceMsgModelViewSet,
    UserInfo,
)
from extras.views import AllStoryModelViewSet, StoryModelViewSet

# from base.models import Profile
# from base.views import ProfileViewSet


router = routers.DefaultRouter()


router.register("persons", UserInfo, basename="persons")
router.register("chats", ChatModelViewSet, basename="chats")
router.register("space", SpaceModelViewSet)
router.register("room-msg", SpaceMsgModelViewSet)
router.register("story", AllStoryModelViewSet)
# router.register("chat-msg", ChatMsgModelViewSet)


# Nested
persons_router = routers.NestedDefaultRouter(router, "persons", lookup="person")
persons_router.register("chats", ChatModelViewSet, basename="person-chats")
persons_router.register("spaces", SpaceModelViewSet, basename="person-spaces")
persons_router.register("stories", StoryModelViewSet, basename="person-story")


# chats
chats_router = routers.NestedDefaultRouter(persons_router, "chats", lookup="chat")
chats_router.register("msgs", ChatMsgModelViewSet, basename="chat-msgs")


# Space
space_router = routers.NestedDefaultRouter(persons_router, "spaces", lookup="space")
space_router.register("msgs", SpaceMsgModelViewSet, basename="space-msgs")


# Story
# story_router = routers.NestedDefaultRouter(persons_router, "stories", lookup="story")
# space_router.register("posts", ChatMsgModelViewSet, basename="space-post")

urlpatterns = router.urls + persons_router.urls + chats_router.urls + space_router.urls
