from rest_framework import serializers
from .models import Rating
from base.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]


class RatingSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Rating
        fields = ["id", "user", "rating"]
