from django.urls import path

from .views import library
from .views import (
    AllBookModelViewSet,
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

from peers_api.urls import router, users_router

router.register("all-stories", AllStoryModelViewSet)
router.register("books", AllBookModelViewSet, basename="books")
router.register("mytasks", MyTaskModelViewSet, basename="mytask")

users_router.register("stories", StoryModelViewSet, basename="user-story")


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
)
