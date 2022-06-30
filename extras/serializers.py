from rest_framework import serializers

from .models import Story


# Story
class AllStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        # fields = ["id", "user", "file", "text", "seen", "created", "updated"]
        fields = "__all__"


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["id", "file", "text", "seen", "created", "updated"]

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        return Story.objects.create(user_id=user_id, **validated_data)
