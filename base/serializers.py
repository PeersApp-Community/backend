from rest_framework import serializers
from base.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ["id", "first_name", "last_name", "email", "phone", "bio", "avatar"]
