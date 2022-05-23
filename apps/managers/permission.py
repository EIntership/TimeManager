from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from apps.managers.models import TimeSetting


class IsManagerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        print(type(request.user))
        if request.user != 'AnonymousUser':
            pass
            # print(TimeSetting.objects.filter(user=request.user, role='Manager'))
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

