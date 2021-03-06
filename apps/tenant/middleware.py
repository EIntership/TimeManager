from django.utils.deprecation import MiddlewareMixin
from rest_framework import permissions

from apps.managers.models import Company
from apps.tenant.helper import set_current_company, set_current_user
from rest_framework_simplejwt import authentication
from django.contrib.auth.models import User


class CompanyMiddleware(MiddlewareMixin):
    @staticmethod
    def company_request(request):
        key = request.headers.get('X-Api-Key') or request.headers.get('x-api-key')
        company = Company.objects.filter(hash=key).first() if key else None
        if company:
            setattr(request, "company", company)
        set_current_company(company)

    @staticmethod
    def user_request(request):
        auth_user = authentication.JWTAuthentication().authenticate(request)
        if request.method in permissions.SAFE_METHODS:
            user = User.objects.all()
        else:
            user = User.objects.filter(username=auth_user[0]).first() if auth_user else None
        if user:
            request.user = user
        set_current_user(user)

    def process_request(self, request):
        self.company_request(request)
        self.user_request(request)
