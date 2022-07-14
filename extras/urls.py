from django.urls import path
from rest_framework_nested import routers
from .views import (
    BookModelViewSet,
    SpaceTaskModelViewSet,
    LibraryModelViewSet,
    MyTaskModelViewSet,
    GenreModelViewSet,
)


router = routers.DefaultRouter()


router.register("sptasks", SpaceTaskModelViewSet, basename="sptask")
router.register("mytasks", MyTaskModelViewSet, basename="mytask")
router.register("lib", LibraryModelViewSet)
router.register("genre", GenreModelViewSet)
# router.register("msg", ThreadModelViewSet)
# router.register("chat-msg", ChatMsgModelViewSet)


# Nested
library_router = routers.NestedDefaultRouter(router, "lib", lookup="lib")
library_router.register("books", BookModelViewSet, basename="lib-books")
# spaces_router.register("library", ProfileModelViewSet, basename="space-library")


# users_router = .NestedDefaultRouter(router, "users", lookup="user")
# users_router.register("chats", ChatModelViewSet, basename="user-chats")

# Profile
# profile_router = routers.NestedDefaultRouter(users_router, "profiles", lookup="profile")
# profile_router.register("posts", ChatMsgModelViewSet, basename="space-post")


urlpatterns = [
    # path("users/<int:user_pk>/chats/del-msgs/", ChatDelMsgMixins.as_view(), name="chat-del-msgs"),
]
