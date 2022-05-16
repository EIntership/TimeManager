from django.urls import path
from rest_framework import routers
from apps.manager.views import CompanyViewSet, GetCompanyViewSet, ProjectViewSet, GetProjectViewSet,TimeViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', CompanyViewSet, basename='company')
router.register(r'', ProjectViewSet, basename='project')
router.register(r'', TimeViewSet, basename='time')
router.register(r'company', GetCompanyViewSet)
router.register(f'project', GetProjectViewSet)

urlpatterns = [

]
urlpatterns += router.urls