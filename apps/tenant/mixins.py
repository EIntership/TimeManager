from django.db import models

from apps.tenant.manager import TenantAwareManager


class TenantAwareModelMixin(models.Model):
    """
    An abstract base class model that provides a foreign key to a tenant
    """
    company = models.ForeignKey("managers.Company", models.CASCADE)
    objects = TenantAwareManager()
    unscoped = models.Manager()

    class Meta:
        abstract = True
