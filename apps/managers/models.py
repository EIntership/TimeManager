from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    user = models.OneToOneField(User, null=True, related_name='company', on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255, null=False)
    member = models.ManyToManyField(User, blank=True, related_name="project", through='managers.TimeSetting')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_projects")


class TimeSetting(models.Model):
    project = models.ForeignKey(Project, related_name="time_settings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_settings")
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
