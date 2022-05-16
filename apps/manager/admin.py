from django.contrib import admin
from apps.manager.models import Project, Company


# Register your models here.


class Project(admin.StackedInline):
    model = Project


@admin.register(Company)
class TaskAdmin(admin.ModelAdmin):
    inlines = [Project]
    list_display = ('name',)

    class Meta:
        model = Company

