from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer, CharField
from apps.managers.models import Company, Project, TimeSetting, ProjectUsers


class TimeSerializer(ModelSerializer):
    user = CharField(read_only=True)

    class Meta:
        model = TimeSetting
        fields = ('id', 'user', 'day', 'month', 'year', 'project')

    def create(self, validated_data):
        request = self.context['request']
        if not ProjectUsers.objects.filter(project_id=request.data['project'], user_id=request.user.id):
            raise PermissionDenied
        return super(TimeSerializer, self).create(validated_data)


class ProjectUserSerializer(ModelSerializer):
    class Meta:
        model = ProjectUsers
        fields = '__all__'


class ProjectSerializer(ModelSerializer):
    users = TimeSerializer(many=True,
                           source='timesetting_set',
                           read_only=True,
                           required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'users')


class CompanySerializer(ModelSerializer):
    company_project = ProjectSerializer(many=True, read_only=True)
    user = CharField(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'user', 'company_project')
