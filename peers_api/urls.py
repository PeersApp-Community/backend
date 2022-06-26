from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RoomModelViewSet,
    RoomMsgModelViewSet,
    ChatModelViewSet,
    StatusModelViewSet,
)

router = DefaultRouter()

router.register("rooms", RoomModelViewSet)
router.register("room-msg", RoomMsgModelViewSet)
router.register("chat", ChatModelViewSet)
router.register("status", StatusModelViewSet)

urlpatterns = router.urls
