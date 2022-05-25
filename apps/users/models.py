import django
from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    @classmethod
    def clear_expiring(cls, seconds=60):
        expiry_time = timezone.now() - datetime.timedelta(seconds=seconds)
        filters = {'timestamp__lte': expiry_time}
        return cls.objects.filter(**filters).delete()

    @classmethod
    def clear_reseted(cls, token):
        return cls.objects.filter(token=token).delete()
