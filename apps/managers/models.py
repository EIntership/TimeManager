from django.contrib.auth.models import User
from django.db import models
from apps.tenant.mixins import TenantAwareModelMixin
import uuid


class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    user = models.OneToOneField(User, null=True, related_name='company', on_delete=models.CASCADE)
    X_API_Key = models.CharField(default=uuid.uuid4().hex, max_length=32)


class Project(TenantAwareModelMixin):
    name = models.CharField(max_length=255, null=False)
    member = models.ManyToManyField(User, blank=True, related_name="project", through='managers.TimeSetting')


class TimeSetting(models.Model):
    project = models.ForeignKey(Project, related_name="time_settings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_settings")
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
