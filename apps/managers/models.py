from django.contrib.auth.models import User
from django.db import models
from apps.tenant.mixins import CompanyAwareModelMixin, UserAwareModelMixin, TimeUserAwareModelMixin
import uuid


class Company(UserAwareModelMixin):
    name = models.CharField(max_length=255, null=False)
    hash = models.CharField(default=uuid.uuid4().hex, max_length=32, editable=False)


class Project(CompanyAwareModelMixin):
    name = models.CharField(max_length=255, null=False)
    users = models.ManyToManyField(User, through='managers.TimeSetting', related_name='user', default=list)


class TimeSetting(TimeUserAwareModelMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
