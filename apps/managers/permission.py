from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.tenant.helper import current_company


class IsCompanyOwner(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        company = current_company()
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(user, AnonymousUser):
            return False
        if user == company.user:
            return True
        return False


class IsManagerOrDeveloperOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.groups.filter(
            Q(name='Developer') | Q(name='Manager')))


class IsAuthenticatedOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not getattr(request, 'user', None):
            return False
        return bool(request.user and request.user.is_active)


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
