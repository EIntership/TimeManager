# Create your views here.
import os
import re
from copy import deepcopy
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_util.decorators import serialize_decorator
from drf_yasg.utils import swagger_auto_schema
import environ
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.users.serializers import UserSerializer, AuthenticationEmailSendSerializer, AuthenticationResetPasswordEmailSerializer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR) + '/.env')


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()
        print(request.user)
        return Response(UserSerializer(user).data)


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
            username = re.findall("\s([A-Za-z0-9._%]+)", uidb64)[0]
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                user.set_password(user_load.get('password'))
                user.save()
                return Response('Password is successful reset ')
        except UnicodeDecodeError:
            return Response('Invalid uidb64')