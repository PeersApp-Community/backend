from django.urls import path

# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    ChatMsgModelViewSet,
    ChatModelViewSet,
    RoomModelViewSet,
    RoomMsgModelViewSet,
    StatusModelViewSet,
    UserInfo,
)

router = routers.DefaultRouter()

router.register("persons", UserInfo, basename="persons")
# router.register("chats", ChatModelViewSet, basename="chats")
router.register("chat-msg", ChatMsgModelViewSet)
router.register("rooms", RoomModelViewSet)
router.register("room-msg", RoomMsgModelViewSet)
router.register("status", StatusModelViewSet)

# Nested
persons_router =routers.NestedDefaultRouter(router, "persons", lookup="person")
persons_router.register("chats", ChatModelViewSet, basename="person-chats")

# chats
chats_router = routers.NestedDefaultRouter(persons_router, "chats", lookup="chat")
chats_router.register("msgs", ChatMsgModelViewSet, basename="chat-msgs")
# chats_router.register("images", views.chatImageViewSet, basename="chat-images")

urlpatterns = [
    # path("users/<int:pk>/chats", None)
]

urlpatterns += router.urls + chats_router.urls + persons_router.urls
