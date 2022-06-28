from django.urls import path

# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    ChatMsgModelViewSet,
    ChatModelViewSet,
    RoomModelViewSet,
    RoomMsgModelViewSet,
    StatusModelViewSet,
)

router = routers.DefaultRouter()

router.register("chats", ChatModelViewSet, basename="chats")
router.register("chat-msg", ChatMsgModelViewSet)
router.register("rooms", RoomModelViewSet)
router.register("room-msg", RoomMsgModelViewSet)
router.register("status", StatusModelViewSet)

# Nested

chats_router = routers.NestedDefaultRouter(router, "chats", lookup="chat")
chats_router.register("msgs", ChatMsgModelViewSet, basename="chat-msgs")
# chats_router.register("images", views.chatImageViewSet, basename="chat-images")


urlpatterns = router.urls
