from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from drf_util.views import BaseModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.managers.serializers import CompanySerializer, ProjectSerializer, TimeSerializer
from apps.managers.models import Company, Project, TimeSetting
from apps.managers.permission import IsManagerOrReadOnly, IsAuthenticatedOrReadOnly


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


class ProjectViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    @action(detail=True,
            methods=['GET'],
            permission_classes=[IsManagerOrReadOnly],
            url_path='statistic')
    def statistic(self, request, pk=None):
        statistics = TimeSetting.objects.filter(project=pk).values('user__groups__name').annotate(Day=Sum('day'), Month=Sum('month'),
                                                                                                  Year=Sum('year'))
        return Response({'statistics': statistics})

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsManagerOrReadOnly, AllowAny),
            url_path='statistic')
    def statistic_all(self, request):
        statistics = TimeSetting.objects.filter().values('user__groups__name').annotate(Day=Sum('day'), Month=Sum('month'),
                                                                                        Year=Sum('year'))
        return Response({'statistics': statistics})


class TimeManagerViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = TimeSerializer
    queryset = TimeSetting.objects.all()
    permission_classes = [IsManagerOrReadOnly]
