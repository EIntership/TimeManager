from rest_framework.serializers import ModelSerializer
from apps.manager.models import Company, Project, TimeManagerSetting, TimeDeveloperSetting


class TimeManagerSerializer(ModelSerializer):

    class Meta:
        model = TimeManagerSetting
        fields = ('day', 'month', 'year', 'project', 'user')


class TimeDevelopersSerializer(ModelSerializer):

    class Meta:
        model = TimeDeveloperSetting
        fields = ('day', 'month', 'year', 'project', 'user')


class ProjectSerializer(ModelSerializer):
    manager_time = TimeManagerSerializer(many=True, read_only=True)
    developer_time = TimeDevelopersSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'manager_time', 'developer_time', 'company')


class CompanySerializer(ModelSerializer):
    company_project = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'user', 'company_project')
