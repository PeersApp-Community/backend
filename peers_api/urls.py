from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    OrganisationModelViewSet,
    RoomModelViewSet,
    RoomChatModelViewSet,
    FriendChatModelViewSet,
    StatusModelViewSet,
)

router = DefaultRouter()

router.register("orgs", OrganisationModelViewSet)
router.register("rooms", RoomModelViewSet)
router.register("room-chats", RoomChatModelViewSet)
router.register("friendchat", FriendChatModelViewSet)
router.register("status", StatusModelViewSet)

urlpatterns = router.urls
