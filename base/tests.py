# from django.test import TestCase

# Create your tests here.
# importing the client from the twilio
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio account


account_sid = "AC46eb2ae7ab874b8fd3c1307574ff3dc3"
auth_token = "140f71b42196cb4e653b7dcb8d750383"
client = Client(account_sid, auth_token)


# def send_otp(otp, VERIFIED_NUMBER):
message = client.messages.create(
    body=f"Your OTP is 898989", from_="+2347066367867", to=["+2347066367867"]
)
# send_otp(otp, validated_data["phone"])
message()
print(message())