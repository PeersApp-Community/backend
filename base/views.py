from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Profile, User
from rest_framework import status
from rest_framework.response import Response
from .serializers import GetOtpSerializer, ProfileSerializer, UserCreateSerializer
import random
import math


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


@api_view(["PATCH"])
@permission_classes([AllowAny])
def validate_user(request):
    if request.method == "PATCH":
        serializer = GetOtpSerializer(data=request.data, partial=True)
        # set partial=True to update a data partially
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"Message": "You are Validated"}, status=status.HTTP_201_CREATED
        )


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

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


# class ValidateUser(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = GetOtpSerializer
#     permission_classes = [AllowAny]
#     http_method_names = ["patch"]
