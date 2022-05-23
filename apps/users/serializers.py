from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password",)


class AuthenticationEmailSendSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ('email',)


class AuthenticationResetPasswordEmailSerializer(serializers.ModelSerializer):
    uidb64 = serializers.CharField(read_only=False)

    class Meta:
        model = User
        fields = ('uidb64', 'password')

