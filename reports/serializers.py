from rest_framework import serializers
from .models import Rating
from base.models import Profile, User


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone"]


class RatingSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Rating
        fields = ["id", "user", "rating"]


class DataSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "gender",
            "institution",
            "educational_level",
            "course",
            "location",
        ]
