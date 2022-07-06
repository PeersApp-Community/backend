from django.forms import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from .models import Otp, Profile, User
from rest_framework.response import Response
from .serializers import (
    LoginSerializer,
    PhoneListSerializer,
    ProfileEditSerializer,
    ProfileSerializer,
    RefreshOTPSerializer,
    UserCreateSerializer,
    set_otp,
)
from django.contrib.auth import authenticate, get_user_model


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# class LoginValidateAPIView()
@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid()
    user = authenticate(**serializer.data)
    if user is not None:
        # otp = Otp.objects.get(user_id=request.data["phone"])
        otp = Otp.objects.get(user_id=user.id)
        otp.otp_num = set_otp(request.data["phone"])
        otp.save()

        user.save()
        return Response({"otp": otp.otp_num}, status=status.HTTP_200_OK)

    return Response(
        {"error": "Incorrect credentials"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def refresh_OTP_view(request):
    serializer = RefreshOTPSerializer(data=request.data)

    if serializer.is_valid():
        otp = Otp.objects.select_related("user").get(user__phone=request.data["phone"])
        otp.otp_num = set_otp(request.data["phone"])
        otp.save()
        return Response(
            f" Refresh Successful for {serializer.data}", status=status.HTTP_200_OK
        )

    return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    # http_method_names = [
    #     "get",
    # ]


class ProfileUpdateAPIView(UpdateAPIView):
    serializer_class = ProfileEditSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "id"
    http_method_names = [
        "patch",
    ]

    def get_serializer_context(self):
        try:
            return {"user_id": self.kwargs["id"]}
        except:
            pass


# @api_view(
#     [
#         "POST",
#     ]
# )
# @permission_classes([AllowAny])
# def check_phone_list(request):
#     serializer = PhoneListSerializer(data=request.data)

#     if serializer.is_valid():
#         new_serializer = []
#         users_phone_list = []
#         sliced_users_phone_list_1 = []
#         sliced_users_phone_list_2 = []
#         users_dictionary = dict()
#         users_list = User.objects.only("phone").order_by("id")

#         try:
#             for item in users_list:
#                 num = item.phone
#                 users_phone_list.append(num)

#             for item in users_phone_list:
#                 sliced_users_phone_list_1.append(str(item[-8:]))
#                 sliced_users_phone_list_2.append(str(item[:-8]))

#             for item in serializer.data["phone_list"]:
#                 digits = str(item)[-8:]
#                 new_serializer.append(digits)
#                 if digits in sliced_users_phone_list_1:
#                     print(True)
#                     print(digits)
#                 else:
#                     print(False)
#                     print(digits)

#         except:
#             print(f"==ERRORR==ERRORR=========")
#             pass

#         ultimate = [
#             new_serializer,
#             serializer.data,
#             sliced_users_phone_list_1,
#             sliced_users_phone_list_2,
#             users_phone_list,
#         ]

#         return Response(ultimate, status=status.HTTP_200_OK)

#     print(serializer.errors)
#     return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def check_phone_list(request):
    serializer = PhoneListSerializer(data=request.data)

    if serializer.is_valid():
        new_serializer = []
        users_phone_list = []
        users_dictionary = {}
        print(type(users_dictionary))

        try:
            for item in serializer.data["phone_list"]:
                digits = str(item)[-3:]
                person = (
                    User.objects.filter(phone__endswith=str(digits))
                    .select_related("profile")
                    .values(
                        "id",
                        "phone",
                        "username",
                        "profile__full_name",
                        "profile__bio",
                        "profile__gender",
                        "profile__institution",
                        "profile__educational_level",
                        "profile__course",
                        "profile__location",
                        "profile__avatar",
                    )
                )
                if len(person) > 0:
                    users_dictionary.update({item: person[0]})
                    print(True)
                    print(digits)
                else:
                    users_dictionary.update({item: "person not found"})
                    print(False)
                    print(digits)

                for item in person:
                    print("okay")
        except:
            print(f"==ERRORR==ERRORR=========")
            pass

        print(serializer.data)
        ultimate = [
            serializer.data,
            users_dictionary,
            users_phone_list,
        ]

        return Response(users_dictionary, status=status.HTTP_200_OK)

    print(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)
