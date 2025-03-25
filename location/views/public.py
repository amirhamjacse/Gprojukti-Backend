from django.shortcuts import render
from human_resource_management.models.employee import EmployeeInformation
from location.filters import *
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from user.models import UserAccount
from django.contrib.auth.hashers import make_password
from utils.permissions import *
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db import transaction

from utils.permissions import CheckCustomPermission
from utils.decorators import log_activity

from rest_framework.generics import get_object_or_404   
from utils.response_wrapper import ResponseWrapper
from location.models import Country,Division,District,Area, OfficeLocation
from location.serializers import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from rest_framework.permissions import AllowAny, IsAuthenticated
 
class PublicDistrictViewSet(CustomViewSet):
    queryset = District.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DistrictFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @log_activity
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset()).order_by('name')
        
        serializer = PublicDistrictSerializer(qs, many=True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status=200)


     
class PublicDivisionViewSet(CustomViewSet):
    queryset = Division.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = DivisionSerializer
    permission_classes = [AllowAny]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DivisionFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
     
class PublicAreaViewSet(CustomViewSet):
    queryset = Area.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = AreaWiseShopSerializer
    permission_classes = [AllowAny]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = AreaFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
     
     
    @log_activity
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()

        # page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=qs, many=True)

        # paginated_data = self.get_paginated_response(serializer.data)
        
        # return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
        return ResponseWrapper(data=serializer.data, msg="Success", status=200)


class PublicOfficeLocationViewSet(CustomViewSet):
    queryset = OfficeLocation.objects.all().order_by('name')
    lookup_field = 'slug'
    serializer_class = OfficeLocationSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = OfficeLocationFilter 
    
    def get_permissions(self):
        if self.action in ["list","user_wise_office_location_list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
class PublicDistrictWIseShopViewSet(CustomViewSet):
    queryset = District.objects.filter(is_active = True).order_by('name')
    lookup_field = 'slug'
    serializer_class = DistrictWiseShopSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DistrictFilter 
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]