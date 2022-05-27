from rest_framework.serializers import ModelSerializer, CharField
from apps.managers.models import Company, Project, TimeSetting


class TimeSerializer(ModelSerializer):
    class Meta:
        model = TimeSetting
        fields = ('day', 'month', 'year', 'project', 'user')


class ProjectSerializer(ModelSerializer):
    members = TimeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'members',)


class CompanySerializer(ModelSerializer):
    company_project = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'user', 'company_project')
