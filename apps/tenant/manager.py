from django.db import models
from apps.tenant.helper import current_company_id, current_company


class TenantAwareManager(models.Manager):
    def get_queryset(self):
        project_id = current_company_id()

        if not project_id:
            return self._queryset_class(self.model)

        # If the manager was built from a queryset using
        # SomeQuerySet.as_manager() or SomeManager.from_queryset(),
        # we want to use that queryset instead of TenantAwareQuerySet.
        if self._queryset_class != models.QuerySet:
            return super().get_queryset().filter(company__id=project_id)

        return TenantAwareQuerySet(self.model, using=self._db).filter(
            company__id=project_id
        )


class TenantAwareQuerySet(models.QuerySet):

    def create(self, **kwargs):
        company_id = current_company_id()
        if company_id and not (kwargs.get('company_id', None) or kwargs.get('company', None)) and self.model.company_id:
            kwargs.update({'company_id': current_company_id()})
        return super().create(**kwargs)

    def get(self, **kwargs):
        company_id = current_company_id()
        if company_id and not (kwargs.get('company_id', None) or kwargs.get('company', None)) and self.model.company_id:
            kwargs.update({'company_id': current_company_id()})
        return super().get(**kwargs)

    def update(self, **kwargs):
        company_id = current_company_id()
        if company_id and not (kwargs.get('company_id', None) or kwargs.get('company', None)) and self.model.company_id:
            kwargs.update({'company_id': current_company_id()})
        return super().update(**kwargs)

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        objs = list(objs)
        for o in objs:
            o.tenant = current_company()

        super().bulk_create(objs, batch_size, ignore_conflicts)

    def as_manager(cls):
        manager = TenantAwareManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True

    as_manager = classmethod(as_manager)
