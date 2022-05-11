# Create your views here.
from copy import deepcopy
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from apps.user.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.user.serializers import AuthenticationRegisterSerializer, AuthenticationLoginSerializer
from django.core.mail import EmailMessage
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
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
            if user:
                email = EmailMessage(
                    'Registration to TimeManager',
                    f'{user.username} thank you for registration',
                    'eugenshow83@gmail.com',
                    [f'{user.email}'],

                )
                email.fail_silently = False
                email.send()
            print(user)
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
        return Response(serializer.data)

    @action(detail=False,
            methods=['POST'],
            url_path='refresh',
            url_name='refresh')


    def refresh(self, request, *args, **kwargs):
        return Response({'success': 'We have sent you a link to reset your password'})


