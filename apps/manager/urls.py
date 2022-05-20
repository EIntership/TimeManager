from django.urls import path
from rest_framework import routers
from apps.manager.views import CompanyViewSet, ProjectViewSet, TimeManagerViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'time', TimeManagerViewSet, basename='time_manager')
urlpatterns = [

]
urlpatterns += router.urls