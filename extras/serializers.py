from rest_framework import serializers

from .models import Story


# import base64

# from django.core.files.base import ContentFile


# class Base64ImageField(serializers.ImageField):
#     def from_native(self, data):
#         if isinstance(data, basestring) and data.startswith("data:image"):
#             # base64 encoded image - decode
#             format, imgstr = data.split(";base64,")  # format ~= data:image/X,
#             ext = format.split("/")[-1]  # guess file extension

#             data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

#         return super(Base64ImageField, self).from_native(data)


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
