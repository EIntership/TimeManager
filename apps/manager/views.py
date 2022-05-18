from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from drf_util.views import BaseModelViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.manager.serializers import CompanySerializer, ProjectSerializer, TimeManagerSerializer, TimeDevelopersSerializer
from apps.manager.models import Company, Project, TimeManagerSetting, TimeDeveloperSetting
from rest_framework.permissions import AllowAny


# Create your views here.


# BasicModelViewSet


class BasicModelViewSet(BaseModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', ]
    search_fields = ['id', ]
    ordering_fields = ['id', ]
    ordering = ['-id', ]

# Company


class CompanyViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

# Project


class ProjectViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @action(detail=True,
            methods=['GET'],
            permission_classes=[AllowAny],
            url_path='statistic')
    def statistic(self, request, pk=None):
        try:
            serializer = self.get_serializer(Project.objects.get(id=pk))
            return Response({'planner_hours_month_developers': self.hours(serializer.data['developer_time'][0]),
                             'planner_hours_month_managers': self.hours(serializer.data['manager_time'][0]),
                             'project': serializer.data})
        except Exception:
            return Response('Project matching query does not exist.')

    @staticmethod
    def hours(time):
        hr = (time['day']*24)+(time['month']*730)+(time['year']*8765)
        if hr >= 730:
            return f'{hr/730} m'
        return f'{hr} h'


class TimeManagerViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = TimeManagerSerializer
    queryset = TimeManagerSetting.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()


class TimeDeveloperViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = TimeDevelopersSerializer
    queryset = TimeDeveloperSetting.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

