from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from .models import Profile, User
import random
import math


def otp_create(phone):
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

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "User with the given phone number already exists."
            )
        if len(value) < 7:
            raise serializers.ValidationError("Phone Number is too short")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.otp = otp_create(validated_data["phone"])
        user.is_active = False
        user.save()
        return user


class GetOtpSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["otp", "phone"]

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "No user with the given phone number was found."
            )
        return value

    def save(self, **kwargs):
        phone = self.validated_data["phone"]
        otp = self.validated_data["otp"]

        try:
            user = User.objects.get(phone=phone, otp=otp)

            # updating an existing user
            self.instance = user
            if self.instance.is_phone_verified == False:
                self.instance.is_phone_verified = True
                self.instance.otp = ""
                self.instance.is_active = True
                self.instance.save()
            return self.instance
        except User.DoesNotExist:
            raise serializers.ValidationError("The OTP is Wrong.")

        # return self.instance


class UserSimpleerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSimpleerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Profile
        fields = "__all__"
        fields = ["id", "user", "first_name", "last_name", "bio", "avatar"]


class ProfileEditSerializer(serializers.ModelSerializer):
    # user = UserSimpleerializer(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Profile
        fields = "__all__"
        fields = ["first_name", "last_name", "bio", "avatar"]

    def save(self, **kwargs):
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        try:
            user = User.objects.get(user_id=self.context["user_id"])
            print(
                """
               ============= lodsafjnjfdsan
               ====== asdfjsdfl;kajdsfk
                =======adskfsjdfk;ads;lf
               ========== dsafjskd;fj';adsf
                ===========asdflasmdf;a
                """
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return super().save(**kwargs)
        except:
            print("error")

    # def create(self, validated_data):
    #     user_id = self.context["user_id"]
    #     return Profile.objects.create(user_id=user_id, **validated_data)


# def send_otp(otp, VERIFIED_NUMBER):
#     client.messages.create(
#         body=f"Your OTP is {otp}", from_="+2348069051233", to=[VERIFIED_NUMBER]
#     )

# send_otp(otp, validated_data["phone"])
#
#
#

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#
# def create(self, validated_data):
#     user = User(
#         username=validated_data['username']
#     )
#     user.set_password(make_password(validated_data['password']))
#     user.save()
#     return user
#
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
#
#
#
