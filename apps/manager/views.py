from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_util.views import BaseModelViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.manager.serializers import CompanySerializer, ProjectSerializer, TimeSerializer
from apps.manager.models import Company, Project, TimeSetting
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


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
        statistics = TimeSetting.objects.filter(project=pk).values('role').annotate(Day=Sum('day'), Month=Sum('month'), Year=Sum('year'))
        return Response({'statistics': statistics})

    @action(detail=False,
            methods=['GET'],
            permission_classes=[AllowAny],
            url_path='statistic')
    def statistic_all(self, request):
        statistics = TimeSetting.objects.filter().values('role').annotate(Day=Sum('day'), Month=Sum('month'),
                                                                          Year=Sum('year'))
        return Response({'statistics': statistics})


class TimeManagerViewSet(BasicModelViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = TimeSerializer
    queryset = TimeSetting.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()
