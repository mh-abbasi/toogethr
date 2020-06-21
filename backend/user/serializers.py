from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all()
            )
        ]
    )
    password = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False
    )
    first_name = serializers.CharField(
        required=False,
        allow_null=False,
        allow_blank=False
    )
    last_name = serializers.CharField(
        required=False,
        allow_null=False,
        allow_blank=False
    )

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user


class ParkingLotTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_superuser'] = user.is_superuser

        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']
