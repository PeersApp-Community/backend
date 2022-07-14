from rest_framework import serializers

from .models import MyTask, Story, Library, Book, Genre, SpaceTask, MyTask


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
        fields = ["__all__"]


# MyTaskSerializer
class MyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTask
        fields = ["__all__"]


# BookSerializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["__all__"]


# GenreSerializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["__all__"]


# SpaceTaskSerializer
class SpaceTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceTask
        fields = ["__all__"]
