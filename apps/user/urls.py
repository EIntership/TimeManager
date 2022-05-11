from django.urls import path
from rest_framework import routers

from apps.user.views import AuthenticationViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', AuthenticationViewSet, basename='authentication')
urlpatterns = [
    # path('request-reset-email/', RequestPasswordResetEmail.as_view(),
    #      name="request-reset-email"),
]
urlpatterns += router.urls