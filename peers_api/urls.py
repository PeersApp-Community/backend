from rest_framework_nested import routers
from .views import (
    ChatMsgModelViewSet,
    ChatModelViewSet,
    SpaceModelViewSet,
    SpaceMsgModelViewSet,
    StoryModelViewSet,
    UserInfo,
)


router = routers.DefaultRouter()


router.register("persons", UserInfo, basename="persons")
# router.register("chats", ChatModelViewSet, basename="chats")
# router.register("chat-msg", ChatMsgModelViewSet)
router.register("space", SpaceModelViewSet)
router.register("room-msg", SpaceMsgModelViewSet)
router.register("status", StoryModelViewSet)


# Nested
persons_router = routers.NestedDefaultRouter(router, "persons", lookup="person")
persons_router.register("chats", ChatModelViewSet, basename="person-chats")
persons_router.register("spaces", ChatModelViewSet, basename="person-spaces")


# chats
chats_router = routers.NestedDefaultRouter(persons_router, "chats", lookup="chat")
chats_router.register("msgs", ChatMsgModelViewSet, basename="chat-msgs")


# Space
space_router = routers.NestedDefaultRouter(persons_router, "spaces", lookup="space")
space_router.register("msgs", ChatMsgModelViewSet, basename="space-msgs")


urlpatterns = router.urls + persons_router.urls + chats_router.urls + space_router.urls
