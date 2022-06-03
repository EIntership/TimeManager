from rest_framework import routers
from apps.managers.views import CompanyViewSet, ProjectViewSet, TimeManagerViewSet, ProjectUserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'project-users', ProjectUserViewSet, basename='project-users')
router.register(r'time', TimeManagerViewSet, basename='time')

urlpatterns = [
    *router.urls
]
