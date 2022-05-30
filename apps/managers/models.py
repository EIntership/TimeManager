from django.contrib.auth.models import User
from django.db import models
from apps.tenant.mixins import CompanyAwareModelMixin, UserAwareModelMixin
import uuid


class Company(UserAwareModelMixin):
    name = models.CharField(max_length=255, null=False)
    hash = models.CharField(default=uuid.uuid4().hex, max_length=32, editable=False)


class Project(CompanyAwareModelMixin):
    name = models.CharField(max_length=255, null=False)
    member = models.ManyToManyField(User, blank=True, related_name="project", through='managers.TimeSetting')


class TimeSetting(models.Model):
    project = models.ForeignKey(Project, related_name="time_settings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_settings")
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
