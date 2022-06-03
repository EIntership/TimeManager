from drf_util.utils import gt
from threading import local

threadlocal = local()
threadlocalcompany = local()


def set_current_company(company):
    setattr(threadlocalcompany, "company", company)


def current_company():
    return getattr(threadlocalcompany, "company", None)


def current_company_id():
    return gt(current_company(), 'id')


def set_current_user(user):
    setattr(threadlocal, "user", user)


def current_user():
    return getattr(threadlocal, "user", None)


def current_user_id():
    return gt(current_user(), 'id')


