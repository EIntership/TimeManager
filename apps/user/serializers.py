from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from apps.user.models import User
from rest_framework import serializers


class AuthenticationRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password",)


class AuthenticationLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    @staticmethod
    def get_tokens(obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        return {
            'email': user.email,
            'tokens': user.tokens
        }


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


