from django.db import models
from django.contrib.auth.models import User
from apps.tenant.manager import CompanyAwareManager, UserAwareManager


# class BaseAwareModelMixin(models.Model):
#     """
#         An abstract base class model that provides a foreign key to a tenant
#     """
#     unscoped = models.Manager()
#
#     class Meta:
#         abstract = True


class CompanyAwareModelMixin(models.Model):
    company = models.ForeignKey("managers.Company", models.CASCADE)
    objects = CompanyAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True


class UserAwareModelMixin(models.Model):
    user = models.OneToOneField(User, models.CASCADE, null=True)
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
