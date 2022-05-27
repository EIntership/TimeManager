from django.utils.deprecation import MiddlewareMixin
from apps.managers.models import Company
from apps.tenant.helper import set_current_company
from copy import deepcopy


class CompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        key = request.headers.get('X-Api-Key') or request.headers.get('x-api-key')
        company = Company.objects.filter(X_API_Key=key).first() if key else None
        set_current_company(company)
