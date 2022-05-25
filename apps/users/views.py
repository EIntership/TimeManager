import uuid
from copy import deepcopy
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from rest_framework import status
from apps.users.models import UserToken
from drf_util.decorators import serialize_decorator
from drf_yasg.utils import swagger_auto_schema
from config.settings import env
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.utils.translation import ugettext_lazy as _
from apps.users.serializers import (UserSerializer,
                                    AuthenticationEmailSendSerializer,
                                    AuthenticationResetPasswordEmailSerializer)


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        user_load = deepcopy(request.data)
        serializer = UserSerializer(data=user_load)
        serializer.is_valid()
        data = serializer.data
        user = User.objects.create(first_name=data.get('first_name'),
                                   last_name=data.get('last_name'),
                                   email=data.get('email'),
                                   username=data.get('username'))
        user.set_password(user_load['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            user = User.objects.filter(email=email).first()
            token, odj = UserToken.objects.update_or_create(user=user, defaults={'token': uuid.uuid4().hex})
            if token:
                email = EmailMessage(
                    _('Time Manager'),
                    _(f'your password reset token %(token)s') % {
                        'token': token.token
                    },
                    env('EMAIL'),
                    [f'{email}'],
                )
                email.fail_silently = False
                email.send()
                return Response({'success': _('We have sent you a link to reset your password.')}, status=status.HTTP_200_OK)
        else:
            return Response(_("This email doesn't exist"),status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['PATCH'],
            url_path='password-reset',
            url_name='password-reset')
    @swagger_auto_schema(request_body=AuthenticationResetPasswordEmailSerializer)
    def password_reset(self, request, *args, **kwargs):
        try:
            user_load = deepcopy(request.data)
            delete = UserToken()
            delete.clear_expiring()
            token = UserToken.objects.filter(token=user_load['token']).first()
            try:
                if User.objects.filter(username=token.user).exists():
                    user = User.objects.filter(username=token.user).first()
                    user.set_password(user_load['password'])
                    user.save()
                    delete.clear_reseted(user_load['token'])
                return Response(_('Password is successful reset'), status=status.HTTP_200_OK)
            except AttributeError:
                return Response(_('Token timed out'), status=status.HTTP_408_REQUEST_TIMEOUT)
        except UnicodeDecodeError:
            return Response(_('Invalid token'), status=status.HTTP_400_BAD_REQUEST)
