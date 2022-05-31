from rest_framework.serializers import ModelSerializer, CharField
from apps.managers.models import Company, Project, TimeSetting
from apps.users.serializers import UserSerializer


class TimeSerializer(ModelSerializer):
    user = CharField(read_only=True)

    class Meta:
        model = TimeSetting
        fields = ('id', 'user', 'day', 'month', 'year', 'project')


class ProjectSerializer(ModelSerializer):
    currencies = TimeSerializer(many=True,
                                source='timesetting_set.all',
                                read_only=True,
                                required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'currencies')


class CompanySerializer(ModelSerializer):
    company_project = ProjectSerializer(many=True, read_only=True)
    user = CharField(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'user', 'company_project')
