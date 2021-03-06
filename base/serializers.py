from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from .models import Otp, Profile, User
import random
import math


def set_otp(phone):
    num = []
    num[:0] = str(phone)
    random_num = int(num[1] + num[3] + num[2] + num[5] + num[4])

    digits = [i for i in range(0, random_num)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])

    return otp


class UserCreateSerializer(DjoserUserCreateSerializer):
    otp = serializers.CharField(read_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "phone", "password", "otp"]

    # otp = serializers.SerializerMethodField(
    #     method_name='get_otp')

    # def get_otp(self, user: User):
    #     return user.otp.otp_num

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "User with the given phone number already exists."
            )
        if len(value) < 7:
            raise serializers.ValidationError("Phone Number is too short")
        return value

    def create(self, validated_data):
        my_phone = validated_data["phone"]
        user = User.objects.create_user(**validated_data)
        user.save()
        otp = Otp.objects.get(user__phone=my_phone)
        otp.otp_num = set_otp(my_phone)
        otp.save()

        return user


class UserSimpleerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone"]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "password"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSimpleerializer()


    class Meta:
        model = Profile
        fields = "__all__"
        fields = [
            "id",
            "user_id",
            "user",
            "full_name",
            "bio",
            "gender",
            "institution",
            "educational_level",
            "course",
            "location",
            "updated",
            "avatar",
        ]


class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "bio",
            "gender",
            "institution",
            "educational_level",
            "course",
            "location",
            "avatar",
            "updated",
        ]

    # def save(self, **kwargs):
    #     first_name = self.validated_data["first_name"]
    #     last_name = self.validated_data["last_name"]

    #     print(kwargs)
    #     print(self.context)
    #     print("=================================")
    #     try:
    #         user = User.objects.get(id=self.context["user_id"])
    #         user.first_name = first_name
    #         user.last_name = last_name
    #         user.save()
    #         return super().save(**kwargs)
    #     except:
    #         raise ValueError("error")


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]


class RefreshOTPSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "phone",
        ]

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "No user with the given credentials exists."
            )
        return value



class PhoneListSerializer(serializers.Serializer):
    phone_list = serializers.ListField()
    

    
# ===================================================
# ===================================================
# ===================================================


# def send_otp(otp, VERIFIED_NUMBER):
#     client.messages.create(
#         body=f"Your OTP is {otp}", from_="+2348069051233", to=[VERIFIED_NUMBER]
#     )

# send_otp(otp, validated_data["phone"])

# class GetOtpSerializer(serializers.ModelSerializer):
# phone = serializers.CharField()
# otp = serializers.CharField(max_length=6, min_length=6, write_only=True)

# class Meta:
#     model = User
#     fields = ["otp", "phone"]

# def validate_phone(self, value):
#     if not User.objects.filter(phone=value).exists():
#         raise serializers.ValidationError(
#             "No user with the given phone number was found."
#         )
#     return value

# def save(self, **kwargs):
#     phone = self.validated_data["phone"]
#     otp = self.validated_data["otp"]

#     try:
#     user = User.objects.get(phone=phone, otp=otp)

#     # updating an existing user
#     self.instance = user
#     if self.instance.is_phone_verified == False:
#         self.instance.is_phone_verified = True
#         self.instance.otp = ""
#         # self.instance.is_active = True
#         self.instance.save()
#     return self.instance
# except User.DoesNotExist:
#     raise serializers.ValidationError("The OTP is Wrong.")
