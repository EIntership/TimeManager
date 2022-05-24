from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class IsManagerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.groups.filter(
            Q(name__startswith='Developer') | Q(name__startswith='Manager')))


class IsAuthenticatedOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
