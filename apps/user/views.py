# Create your views here.
import re
from copy import deepcopy
from django.db import IntegrityError
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.viewsets import ViewSet
from apps.user.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.user.serializers import (AuthenticationRegisterSerializer,
                                   AuthenticationLoginSerializer,
                                   AuthenticationEmailSendSerializer,
                                   AuthenticationResetPasswordEmailSerializer)
from django.core.mail import EmailMessage
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import environ
import os


# Initialise environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR) + '/.env')

# Create your views here.


class AuthenticationViewSet(ViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = AuthenticationRegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @action(detail=False,
            methods=['POST'],
            url_path='register',
            url_name='register')
    @swagger_auto_schema(request_body=AuthenticationRegisterSerializer)
    def register(self, request, *args, **kwargs):
        try:
            user_load = deepcopy(request.data)
            serializer = AuthenticationRegisterSerializer(data=user_load)
            serializer.is_valid()
            data = serializer.data
            user = User.objects.create(email=data.get('email'),
                                       username=data.get('username'))
            user.set_password(user_load.get('password'))
            user.save()
            print(type(user))
            if user:
                email = EmailMessage(
                    env('EMAIL_REGISTER'),
                    f'{user.username} thank you for registration',
                    env('EMAIL'),
                    [f'{user.email}']
                )
                email.fail_silently = False
                email.send()
            return Response(AuthenticationRegisterSerializer(user).data)
        except IntegrityError:
            return Response('This user already exist')

    @action(detail=False,
            methods=['POST'],
            url_path='login',
            url_name='login')
    @swagger_auto_schema(request_body=AuthenticationLoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = AuthenticationLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        print(serializer.is_valid(raise_exception=False))
        return Response(serializer.data)


class PasswordResetViewSet(ViewSet):
    http_method_names = ('get', 'patch', 'post', 'delete',)
    serializer_class = AuthenticationEmailSendSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @action(detail=False,
            methods=['POST'],
            url_path='email-password-reset',
            url_name='email-password-reset')
    @swagger_auto_schema(request_body=AuthenticationEmailSendSerializer)
    def token_email_send(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user))
            if uidb64:
                email = EmailMessage(
                   env('EMAIL_TOKEN'),
                    f'your password reset token {uidb64}',
                    env('EMAIL'),
                    [f'{email}'],
                )
                email.fail_silently = False
                email.send()
                return Response({'success': 'We have sent you a link to reset your password'})
        else:
            return Response({'This email doesn t exist'})

    @action(detail=False,
            methods=['PATCH'],
            url_path='password-reset',
            url_name='password-reset')
    @swagger_auto_schema(request_body=AuthenticationResetPasswordEmailSerializer)
    def password_reset(self, request, *args, **kwargs):
        try:
            user_load = deepcopy(request.data)
            uidb64 = urlsafe_base64_decode(request.data.get('uidb64')).decode("utf-8")
            print(uidb64)
            email = re.search("(([a-z0-9._%]+)@([a-z0-9._-]+\.[a-z]{2,}))",uidb64)[0]
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.set_password(user_load.get('password'))
                user.save()
                return Response('Password is successful reset ')
        except UnicodeDecodeError:
            return Response('Invalid uidb64')







