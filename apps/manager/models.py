from django.db import models
#from apps.User.models import User

# Create your models here.

#
# class Project(models.Model):
#     name = models.CharField(max_length=255, null=False)
#     hours = models.IntegerField(null=False, default=1)
#     project_managers = models.ManyToManyField(user, blank=True, related_name="managers")
#     project_developers = models.ManyToManyField(user, blank=True, related_name="developers")
#
#     def __str__(self):
#         return self.name
#
#
# class Company(models.Model):
#     name = models.CharField(max_length=255, null=False)
#     project = models.ManyToManyField(Project)
