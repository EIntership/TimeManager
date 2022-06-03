from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from drf_util.views import BaseModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from apps.managers.serializers import CompanySerializer, ProjectSerializer, TimeSerializer, ProjectUserSerializer
from apps.managers.models import Company, Project, TimeSetting, ProjectUsers
from apps.managers.permission import IsManagerOrDeveloperOrReadOnly, IsAuthenticatedOrReadOnly, IsCompanyOwner


class BasicModelViewSet(BaseModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', ]
    search_fields = ['id', ]
    ordering_fields = ['id', ]
    ordering = ['-id', ]


class CompanyViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProjectUserViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = ProjectUserSerializer
    queryset = ProjectUsers.objects.all()
    permission_classes = [IsCompanyOwner]


class ProjectViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsManagerOrDeveloperOrReadOnly]

    @action(detail=True,
            methods=['GET'],
            url_path='user/statistic')
    def user_statistic(self, request, pk=None):
        statistics = TimeSetting.objects.filter(project=pk).values('user__groups__name').annotate(Day=Sum('day'),
                                                                                                  Month=Sum('month'),
                                                                                                  Year=Sum('year'))
        return Response({'statistics': statistics})

    @action(detail=False,
            methods=['GET'],
            url_path='user/statistic')
    def all_statistic_user(self, request):
        statistics = TimeSetting.objects.filter().values('user__groups__name').annotate(Day=Sum('day'),
                                                                                        Month=Sum('month'),
                                                                                        Year=Sum('year'))
        return Response({'statistics': statistics})


class TimeManagerViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = TimeSerializer
    queryset = TimeSetting.objects.all()
    permission_classes = [IsManagerOrDeveloperOrReadOnly]
    ordering = ['user', ]




