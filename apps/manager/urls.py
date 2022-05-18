from django.urls import path
from rest_framework import routers
from apps.manager.views import CompanyViewSet, ProjectViewSet, TimeManagerViewSet, TimeDeveloperViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'time/manager', TimeManagerViewSet, basename='time_manager')
router.register(r'time/developer', TimeDeveloperViewSet, basename='time_developer')
urlpatterns = [

]
urlpatterns += router.urls