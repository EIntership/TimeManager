from django.db import models
from django.contrib.auth.models import User
from apps.tenant.manager import CompanyAwareManager, UserAwareManager


class CompanyAwareModelMixin(models.Model):
    """
    An abstract base class model that provides a foreign key to a tenant
    """
    company = models.ForeignKey("managers.Company", models.CASCADE)
    objects = CompanyAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True


class UserAwareModelMixin(models.Model):
    """
    An abstract base class model that provides a foreign key to a tenant
    """
    user = models.OneToOneField(User, models.CASCADE, null=True, unique=True)
    objects = UserAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True
