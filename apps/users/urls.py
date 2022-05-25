from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from apps.users.views import RegisterUserView, PasswordResetViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', PasswordResetViewSet, basename='authentication')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token-register'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    *router.urls
]
