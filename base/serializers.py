from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from .models import Profile, User
import random
import math

# importing the client from the twilio
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio account


account_sid = "AC46eb2ae7ab874b8fd3c1307574ff3dc3"
auth_token = "140f71b42196cb4e653b7dcb8d750383"
client = Client(account_sid, auth_token)


def send_otp(otp, VERIFIED_NUMBER):
    client.messages.create(
        body=f"Your OTP is {otp}", from_="+2348069051233", to=[VERIFIED_NUMBER]
    )
    
# send_otp(otp, validated_data["phone"])



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


# class UserCreateSerializer(DjoserUserCreateSerializer):
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta(DjoserUserCreateSerializer.Meta):
        # model = User
        fields = ["id", "username", "email", "phone", "password"]

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "User with the given phone number already exists."
            )
        if len(value) < 7:
            raise serializers.ValidationError("Phone Number is too short")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.otp = otp_create(validated_data["phone"])
        user.save()
        otp = user.otp
        send_otp(otp, validated_data["phone"])
        return user

    # def update(self, instance, validated_data):

    #     return super().update(instance, validated_data)

    # def create(self, vali):
    #     serializer = UserCreateSerializer(data=request.data)

    #     if serializer.is_valid(raise_exception=True):
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
                self.instance.save()
            return self.instance
        except User.DoesNotExist:
            raise serializers.ValidationError("The OTP is Wrong.")

        # return self.instance

    #

    # def save(self, **kwargs):
    #     otp = self.validated_data['otp']

    #     # phone = Customer.objects.get(
    #     #     phone=self.context['phone'])
    #     User = Order.objects.create(customer=customer)

    #     cart_items = CartItem.objects \
    #         .select_related('product') \
    #         .filter(cart_id=cart_id)
    #     order_items = [
    #         OrderItem(
    #             order=order,
    #             product=item.product,
    #             unit_price=item.product.unit_price,
    #             quantity=item.quantity
    #         ) for item in cart_items
    #     ]
    #     OrderItem.objects.bulk_create(order_items)

    #     Cart.objects.filter(pk=cart_id).delete()

    #     order_created.send_robust(self.__class__, order=order)

    #     return order


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ["id", "user_id", "first_name", "last_name", "bio", "avatar"]

    def create(self, validated_data):
        user_id = self.context["user_id"]
        return Profile.objects.create(user_id=user_id, **validated_data)
