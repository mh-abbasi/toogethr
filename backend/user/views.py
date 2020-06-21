from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import (
    UserRegisterSerializer,
    ParkingLotTokenObtainPairSerializer,
    UserProfileSerializer
)


class RegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(None, status=status.HTTP_201_CREATED)


class ParkingLotTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = ParkingLotTokenObtainPairSerializer


class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
