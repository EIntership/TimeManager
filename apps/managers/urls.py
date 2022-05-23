from rest_framework import routers
from apps.managers.views import CompanyViewSet, ProjectViewSet, TimeManagerViewSet, CompanyView
from django.urls import path

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'time', TimeManagerViewSet, basename='time_manager')
urlpatterns = [
    path('companytest', CompanyView.as_view(), name='task-time-log-view'),
]
urlpatterns += router.urls