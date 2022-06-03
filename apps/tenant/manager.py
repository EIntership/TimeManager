from django.db import models, IntegrityError
from apps.tenant.helper import current_company_id, current_company, current_user_id


class BasicAwareQuerySet(models.QuerySet):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        objs = list(objs)
        for o in objs:
            o.tenant = current_company()

        super().bulk_create(objs, batch_size, ignore_conflicts)

    def as_manager(cls):
        manager = CompanyAwareManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True

    as_manager = classmethod(as_manager)


class CompanyAwareManager(models.Manager):
    def get_queryset(self):
        company_id = current_company_id()
        if not company_id:
            return self._queryset_class(self.model)

        # If the manager was built from a queryset using
        # SomeQuerySet.as_manager() or SomeManager.from_queryset(),
        # we want to use that queryset instead of TenantAwareQuerySet.

        if self._queryset_class != models.QuerySet:
            return super().get_queryset().filter(company__id=company_id)

        return CompanyAwareQuerySet(self.model, using=self._db).filter(
            company__id=company_id
        )


class CompanyAwareQuerySet(BasicAwareQuerySet):
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


class UserAwareManager(models.Manager):
    def get_queryset(self):
        user_id = current_user_id()

        if not user_id:
            return self._queryset_class(self.model)

        if self._queryset_class != models.QuerySet:
            return super().get_queryset().filter(user__id=user_id)

        return UserAwareQuerySet(self.model, using=self._db).filter(
            user__id=user_id
        )


class UserAwareQuerySet(BasicAwareQuerySet):
    def create(self, **kwargs):
        user_id = current_user_id()
        if user_id and not (kwargs.get('user_id', None) or kwargs.get('user', None)) and self.model.user_id:
            kwargs.update({'user_id': current_user_id()})
            try:
                return super().create(**kwargs)
            except IntegrityError:
                return super(UserAwareQuerySet, self).get(user_id=user_id)

    def get(self, **kwargs):
        user_id = current_user_id()
        if user_id and not (kwargs.get('user_id', None) or kwargs.get('user', None)) and self.model.user_id:
            kwargs.update({'user_id': current_user_id()})
        return super().get(**kwargs)

    def update(self, **kwargs):
        user_id = current_user_id()
        if user_id and not (kwargs.get('user_id', None) or kwargs.get('user', None)) and self.model.user_id:
            kwargs.update({'user_id': current_user_id()})
        return super().update(**kwargs)
