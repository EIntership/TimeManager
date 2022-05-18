from django.db import models

from apps import manager
from apps.user.models import User


# Create your models here.


class Company(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=255, null=False)
    user = models.OneToOneField(User, null=True, related_name='company', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(max_length=255, null=False)
    managers = models.ManyToManyField(User, blank=True, related_name="managers", through='manager.TimeManagerSetting')
    developers = models.ManyToManyField(User, blank=True, related_name="developers", through='manager.TimeDeveloperSetting')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_project")

    def __str__(self):
        return self.name


class TimeManagerSetting(models.Model):
    project = models.ForeignKey(Project, related_name="manager_time", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Product_Manager")
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)


class TimeDeveloperSetting(models.Model):
    project = models.ForeignKey(Project, related_name="developer_time", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Product_Developer")
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)

