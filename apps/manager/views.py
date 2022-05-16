import json

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_util.views import BaseModelViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.manager.serializers import CompanySerializer, ProjectSerializer, TimeSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from apps.manager.models import Company, Project
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response


# Create your views here.


# Company


class BasicModelViewSet(BaseModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', ]
    search_fields = ['id', ]
    ordering_fields = ['id', ]
    ordering = ['-id', ]


class CompanyViewSet(ViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @action(detail=False,
            methods=['POST'],
            url_path='company/register',
            url_name='company/register')
    @swagger_auto_schema(request_body=CompanySerializer)
    def company(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("ERROR")


class GetCompanyViewSet(BasicModelViewSet):
    http_method_names = ('get',)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (AllowAny,)

# Project


class ProjectViewSet(ViewSet):
    http_method_names = ('get', 'post', 'delete',)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @action(detail=False,
            methods=['POST'],
            url_path='project/register',
            url_name='project/register')
    @swagger_auto_schema(request_body=ProjectSerializer)
    def project(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("ERROR")


class GetProjectViewSet(BasicModelViewSet):
    http_method_names = ('get',)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)


class TimeViewSet(ViewSet):
    http_method_names = ('put',)
    serializer_class = TimeSerializer
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)

    @action(detail=True,
            methods=['PUT'],
            url_path='project/start',
            url_name='project/start')
    @swagger_auto_schema(request_body=TimeSerializer)
    def time(self, request, pk=None):
        data = request.data
        queryset = get_object_or_404(Project.objects.filter(id=pk))
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            print(TimeSerializer(queryset).data)
        return Response("queryset.data")