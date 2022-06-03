from django.db import models
from django.contrib.auth.models import User
from apps.tenant.manager import CompanyAwareManager, UserAwareManager


class CompanyAwareModelMixin(models.Model):
    company = models.ForeignKey("managers.Company", models.CASCADE, blank=True)
    objects = CompanyAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True


class UserAwareModelMixin(models.Model):
    user = models.OneToOneField(User, models.CASCADE, blank=True, null=True)
    objects = UserAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True


class TimeUserAwareModelMixin(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True)
    objects = UserAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True
