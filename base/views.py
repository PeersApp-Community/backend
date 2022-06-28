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
from .models import Profile, User
from rest_framework.response import Response
from .serializers import (
    LoginSerializer,
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
    print("serialize======111=============================")
    serializer = LoginSerializer(data=request.data)
    print("serialize=========222==========================")
    serializer.is_valid()
    print("serialize============333=======================")
    user = authenticate(**serializer.data)
    print("serialize============444=======================")
    if user is not None:
        print(serializer.data)
        print(user)
        print(user.otp + "asfdsaf")
        user.otp = set_otp(user.phone)
        print(user.otp)
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshOtpAPIView(GenericAPIView):
    serializer_class = RefreshOTPSerializer
    queryset = User

    def post(self):
        print("serialize======111=============================")
        serializer = RefreshOtpSerializer(data=self.request.data)
        print("serialize=========222==========================")
        valid = serializer.is_valid()
        print("serialize============333=======================")

        print("serialize============444=======================")
        if valid:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def refresh_OTP_view(request):
    print("serialize======111=============================")
    serializer = RefreshOTPSerializer(data=request.data)
    print("serialize=========222==========================")
    print("serialize============333=======================")

    print("serialize============444=======================")
    if serializer.is_valid():
        user = User.objects.get(phone=request.data["phone"])
        user.otp = set_otp(request.data["phone"])
        user.save()
        return Response(
            f" Refresh Successful for {serializer.data}", status=status.HTTP_200_OK
        )

    return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    # http_method_names = [
    #     "get",
    # ]


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
            print("==============================================")
            print(self)
            print(self.kwargs)
            print("==============================================")
            return {"user_id": self.kwargs["id"]}
        except:
            pass


# @api_view(["PATCH"])
# @permission_classes([AllowAny])
# def updateUserProfile(request, id):
#     serializer = ProfileEditSerializer(data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     user = User.objects.get(id=id)
#     if user.id == id:
#         user.first_name = request.data["first_name"]
#         user.last_name = request.data["last_name"]
#         user.save()
#         serializer.save()
#         print("saving")
#         return Response(serializer.data)
#     return ValidationError("Profile does not match")

# def get_queryset(self):
#     user = self.request.user

#     if user.is_staff:
#         return Profile.objects.all()

#     profile_id = Profile.objects.only(
#         'id').get(user_id=user.id)
#     return Profile.objects.filter(profile_id=profile_id)

# def get_serializer_context(self):
#     return {"user_id": self.request.user.id}

# def create(self, request, *args, **kwargs):
#     serializer = UserCreateSerializer(
#         data=request.data,
#         context={'user_id': self.request.user.id})
#     try:
#         serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     serializer = OrderSerializer(order)
#     return Response(serializer.data)
# def get_queryset(self):
#     return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
# def post(self, request, *args, **kwargs):
#     id = request.user.id
#     return self.create(request, *args, **kwargs)

# def update(self, request, *args, **kwargs):
#     serializer = ProfileEditSerializer(data=request.data, partial=True)

#     serializer.is_valid(raise_exception=True)
#     user = User.objects.get(id=kwargs["id"])
#     if user.id == kwargs["id"]:
#         user.first_name = request.data["first_name"]
#         user.last_name = request.data["last_name"]
#         user.save()
#         serializer.save()
#         return Response(serializer.data)
#     return ValidationError("Profile does not match")


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def user_create(request):
#     if request.method == "POST":
#         serializer = UserCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # return Response("serializer", status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["PATCH"])
# @permission_classes([AllowAny])
# def validate_user(request):
#     if request.method == "PATCH":
#         serializer = GetOtpSerializer(data=request.data, partial=True)
#         # set partial=True to update a data partially
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {"Validation Successful, Happy Learning"}, status=status.HTTP_200_OK
#         )
