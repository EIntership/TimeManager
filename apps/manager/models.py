from django.db import models
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
    day = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    time_start = models.DateTimeField(auto_now_add=False, null=True)
    time_finish = models.DateTimeField(auto_now_add=False, null=True)
    project_managers = models.ManyToManyField(User, blank=True, related_name="managers")
    project_developers = models.ManyToManyField(User, blank=True, related_name="developers")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_project")

    def __str__(self):
        return self.name
