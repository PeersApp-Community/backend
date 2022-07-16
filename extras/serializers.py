from rest_framework import serializers

from .models import MyTask, Story, Library, Book, SpaceTask, MyTask
from peers_api.serializers import UserInfoSimpleSerializer2

# Story
class AllStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        # fields = ["id", "user", "file", "text", "seen", "created", "updated"]
        fields = "__all__"


# StorySerializer
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["id", "file", "text", "seen", "created", "updated"]

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        return Story.objects.create(user_id=user_id, **validated_data)


# LibrarySerializer
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "user_id", "books"]


# MyTaskSerializer
class MyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTask
        fields = "__all__"


# BookSerializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "title",
            "description",
            "file",
            "cover",
            "savers",
            "public",
        ]

    def create(self, validated_data):
        creator_id = self.context.get("user_id")
        return Book.objects.create(creator_id=creator_id, **validated_data)


# SavedBookSerializer
class SavedBookSerializer(serializers.ModelSerializer):
    creator = UserInfoSimpleSerializer2()

    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "title",
            "creator",
            "description",
            "file",
            "cover",
            "savers",
            "public",
        ]


# SavedPatchBookSerializer
class SavedPatchBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["savers"]


# SpaceTaskSerializer
class SpaceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceTask
        fields = "__all__"
