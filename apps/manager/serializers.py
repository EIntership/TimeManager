from rest_framework.serializers import ModelSerializer, DateTimeField, IntegerField
from apps.manager.models import Company, Project


class ProjectSerializer(ModelSerializer):
    time_start = DateTimeField(read_only=True)
    time_finish = DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'day', 'month', 'year', 'time_start', 'time_finish', 'project_managers', 'project_developers', 'company')


class CompanySerializer(ModelSerializer):
    company_project = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'user', 'company_project')


class TimeSerializer(ModelSerializer):
    time_start = DateTimeField(required=False)
    time_finish = DateTimeField(required=False)

    class Meta:
        model = Project
        fields = ('time_start', 'time_finish')

    def validate(self, attrs):
        print(attrs)
        return attrs



