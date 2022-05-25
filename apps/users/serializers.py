from django.contrib.auth.models import User
from rest_framework import serializers
from apps.users.models import UserToken


class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ("user", "token")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")


class AuthenticationEmailSendSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']


class AuthenticationResetPasswordEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=False)

    class Meta:
        model = User
        fields = ('token', 'password')
