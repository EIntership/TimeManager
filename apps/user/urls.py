from django.urls import path
from rest_framework import routers
from apps.user.views import AuthenticationViewSet, PasswordResetViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', AuthenticationViewSet, basename='authentication')
router.register(r'', PasswordResetViewSet, basename='PasswordReset')
urlpatterns = [
]
urlpatterns += router.urls