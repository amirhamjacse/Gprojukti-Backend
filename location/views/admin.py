from django.shortcuts import render
from human_resource_management.models.employee import EmployeeInformation
from location.filters import *
from utils.base import get_user_store_list
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from user.models import UserAccount, UserInformation, UserType
from django.contrib.auth.hashers import make_password
from utils.permissions import *
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db import transaction

from utils.permissions import CheckCustomPermission

from rest_framework.generics import get_object_or_404   
from utils.response_wrapper import ResponseWrapper
from location.models import Country,Division,District,Area, OfficeLocation
from location.serializers import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.decorators import log_activity


class CountryViewSet(CustomViewSet):
    queryset = Country.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = CountrySerializer
    permission_classes = [CheckCustomPermission]

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        name = request.data.get('name')
        country_qs = Country.objects.filter(name=name).last()
        if country_qs:
            return ResponseWrapper(error_msg='Country Name Must Be Unique', error_code=400)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = self.request.user
            qs = serializer.save()

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


class DistrictViewSet(CustomViewSet):
    queryset = District.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = DistrictSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DistrictFilter

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        name = request.data.get('name')
        district_qs = District.objects.filter(name=name).last()
        if district_qs:
            return ResponseWrapper(error_msg='District Name Must Be Unique', error_code=400)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = self.request.user
            qs = serializer.save()

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


class DivisionViewSet(CustomViewSet):
    queryset = Division.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = DivisionSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DivisionFilter

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        name = request.data.get('name')
        division_qs = Division.objects.filter(name=name).last()
        if division_qs:
            return ResponseWrapper(error_msg='Division Name Must Be Unique', error_code=400)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = self.request.user
            qs = serializer.save()

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


class AreaViewSet(CustomViewSet):
    queryset = Area.objects.all()
    lookup_field = 'pk'
    serializer_class = AreaSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = AreaFilter
    
    
    
    def get_permissions(self):
        if self.action in ["create",]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        name = request.data.get('name')
        area_qs = Area.objects.filter(name=name).last()
        if area_qs:
            return ResponseWrapper(error_msg='Area Name Must Be Unique', error_code=400)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = self.request.user
            qs = serializer.save()

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    @log_activity
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()

        # page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=qs, many=True)

        # paginated_data = self.get_paginated_response(serializer.data)
        
        # return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
        return ResponseWrapper(data=serializer.data, msg="Success", status=200)


class OfficeLocationViewSet(CustomViewSet):
    queryset = OfficeLocation.objects.all().order_by('name')
    lookup_field = 'slug'
    serializer_class = OfficeLocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = OfficeLocationFilter

    def get_permissions(self):
        if self.action in ["user_wise_office_location_list"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = OfficeLocationCreateUpdateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = OfficeLocationSerializer
        else:
            self.serializer_class = OfficeLocationListSerializer

        return self.serializer_class
    
    @log_activity
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset()).order_by('name').exclude(
            office_type__in = ["HEAD_OFFICE"]
        )
        
        serializer_class = self.get_serializer_class()

        # page_qs = self.paginate_queryset(qs.order_by('name'))
        # serializer = serializer_class(instance=page_qs, many=True)

        # paginated_data = self.get_paginated_response(serializer.data)
        
        # return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
        serializer_class = self.get_serializer_class()

        # page_qs = self.paginate_queryset(qs.order_by('name'))
        
        serializer = serializer_class(instance=qs, many=True)

        # paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status=200)


    # ..........***.......... Get All Data ..........***..........
    @log_activity
    def user_wise_office_location_list(self, request, *args, **kwargs):
        store_list = get_user_store_list(request_user = request.user).order_by('name')
 
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        
        page_qs = self.paginate_queryset(store_list)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
       
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        name = request.data.get('name')
        if not name:
            return ResponseWrapper(error_msg="Shop Name is Required", error_code=400)
        
        qs = self.queryset.filter(name = name)
        
        if qs:
            return ResponseWrapper(error_msg="Shop Name is Already Found", error_code=400)
        
        slug = unique_slug_generator(name = name)
        
        employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
        
        if not employee_qs or not employee_qs.employee_company:
            return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
        company_id = employee_qs.employee_company
        
        area_qs = Area.objects.filter(slug = str(request.data.get('area'))).last()
        if not area_qs:
            return ResponseWrapper(error_msg='Area is Not Found', error_code=404)
        if not area_qs.pos_areas:
            return ResponseWrapper(error_msg='POS Area is Not Found', error_code=400)
        
        pos_area_name = area_qs.pos_areas.last().name
        
        if area_qs.pos_areas:
            if not area_qs.pos_areas.last().pos_regions:
                return ResponseWrapper(error_msg='POS Region is Not Found', error_code=400)
        
        pos_region_name = area_qs.pos_areas.last().pos_regions.last().name
        
        area = serializer.validated_data.pop('area', None)
        
        qs = serializer.save(
                created_by=request.user,
                slug=slug,
                company=company_id,
                pos_area_name = pos_area_name,
                pos_region_name = pos_region_name,
                area = area_qs, 
            )
        if qs.office_type == 'STORE':
            user_qs = UserAccount.objects.filter(
                Q(phone=qs.primary_phone) 
                | Q(email=qs.email)
            ).last()
            
            if user_qs:
                return ResponseWrapper(error_msg='Shop User is Already Found', error_code=404)
            
        serializer = OfficeLocationSerializer(instance=qs)
        
        return ResponseWrapper(data= serializer.data, msg='Office Location Created', status=200)    
    
    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        name = request.data.get('name')
        is_use_scanner = request.data.get('is_use_scanner')
        
        qs = self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_msg="Office Location is Not Found", error_code=404)
        
        office_location_qs = self.queryset.exclude(slug = qs.slug).filter(slug = slug).last()
        
        if office_location_qs:
            return ResponseWrapper(error_msg="Office Location is Already Found", error_code=404)
        
        employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
        
        # if not employee_qs or not employee_qs.employee_company:
        #     return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
        # company_id = employee_qs.employee_company
        company_id = Company.objects.all().last()
        
        if request.data.get('area'):
        
            area_qs = Area.objects.filter(slug = str(request.data.get('area'))).last()
            if not area_qs:
                return ResponseWrapper(error_msg='Area is Not Found', error_code=404)
            if not area_qs.pos_areas:
                return ResponseWrapper(error_msg='POS Area is Not Found', error_code=400)
            
            try:
                pos_area_name = area_qs.pos_areas.last().name
            except:
                pos_area_name = '-'
            
            if not area_qs.pos_areas.last().pos_regions:
                return ResponseWrapper(error_msg='POS Region is Not Found', error_code=400)
            
            try:
                pos_region_name = area_qs.pos_areas.last().pos_regions.last().name
            except:
                pos_region_name = '-'
            
            area = serializer.validated_data.pop('area', None)
        
        qs = serializer.update(
            instance=qs, 
            validated_data=serializer.validated_data
            )
        
        print('is_use_scanner = ', is_use_scanner)
        qs.updated_by=request.user
        qs.is_use_scanner=is_use_scanner
        qs.save()
        
        serializer = OfficeLocationSerializer(instance=qs)
        return ResponseWrapper(data= serializer.data, msg='Office Location Created', status=200)


class POSAreaViewSet(CustomViewSet):
    queryset = POSArea.objects.all()
    lookup_field = 'slug'
    serializer_class = POSAreaSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = POSAreaFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = POSAreaCreateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = POSAreaSerializer
        else:
            self.serializer_class = POSAreaListSerializer

        return self.serializer_class
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        employee_slug = request.data.pop('employee_slug')
        employee_qs = None
        
        serializer = serializer_class(data=request.data, partial=True)
       
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        name = request.data.get('name')
        if not name:
            return ResponseWrapper(error_msg="POS Area Name is Required", error_code=400)
        
        qs = self.queryset.filter(name = name)
        
        if qs:
            return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
        
        slug = unique_slug_generator(name = name)
        
        
        area_qs = Area.objects.filter(slug = str(request.data.get('area'))).last()
        if not area_qs:
            return ResponseWrapper(error_msg='Area is Not Found', error_code=404)
        
        if employee_slug:
            employee_qs = EmployeeInformation.objects.filter(slug= employee_slug).last()
            if not employee_qs:
                return ResponseWrapper(error_msg='Employee is Not Found', error_code=404)
        
        area = serializer.validated_data.pop('area', None)
        
        qs = serializer.save(
                created_by=request.user,
                slug=slug,
                area = area_qs, 
            )
        
        if employee_qs:
            employee_qs.pos_area = qs
            employee_qs.save()
        
        serializer = POSAreaSerializer(instance=qs)
        
        return ResponseWrapper(data= serializer.data, msg='Success', status=200)    

    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        employee_slug = request.data.pop('employee_slug')
        employee_qs = None
        serializer = serializer_class(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        name = request.data.get('name')
        area_qs = None
        
        qs = self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_msg="POS Area is Not Found", error_code=404)
        
        office_location_qs = self.queryset.exclude(slug = qs.slug).filter(slug = slug).last()
        
        if office_location_qs:
            return ResponseWrapper(error_msg="Area is Already Found", error_code=404)
        
        if request.data.get('area'):
        
            area_qs = Area.objects.filter(slug = str(request.data.get('area'))).last()
            if not area_qs:
                return ResponseWrapper(error_msg='Area is Not Found', error_code=404)
            
            
            area = serializer.validated_data.pop('area', None)

        if employee_slug:
            employee_qs = EmployeeInformation.objects.filter(slug= employee_slug).last()
            if not employee_qs:
                return ResponseWrapper(error_msg='Employee is Not Found', error_code=404)
        
        area = serializer.validated_data.pop('area', None)
        
        qs = serializer.update(
            instance=qs, 
            validated_data=serializer.validated_data
            )
        
        qs.updated_by=request.user
        if area_qs:
            qs.area=area_qs
        qs.save()
        
        if employee_qs:
            employee_qs.pos_area = qs
            employee_qs.save()
        
        serializer = POSAreaSerializer(instance=qs)
        return ResponseWrapper(data= serializer.data, msg='POS Area Updated', status=200)


class POSRegionViewSet(CustomViewSet):
    queryset = POSRegion.objects.all().order_by('-name')
    lookup_field = 'slug'
    serializer_class = POSRegionSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = POSRegionFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = POSRegionCreateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = POSRegionSerializer
        else:
            self.serializer_class = POSRegionListSerializer

        return self.serializer_class

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        employee_slug = request.data.pop('employee_slug')
        employee_qs = None
        
        serializer = serializer_class(data=request.data, partial=True)
        
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        name = request.data.get('name')
        if not name:
            return ResponseWrapper(error_msg="POS Region Name is Required", error_code=400)
        
        qs = self.queryset.filter(name = name)
        
        if qs:
            return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
        
        slug = unique_slug_generator(name = name)
        
        
        pos_area_qs = POSArea.objects.filter(slug = str(request.data.get('pos_area'))).last()
        
        if not pos_area_qs:
            return ResponseWrapper(error_msg='POS Area is Not Found', error_code=404)
        
        pos_area = serializer.validated_data.pop('pos_area', None)
        
        

        if employee_slug:
            employee_qs = EmployeeInformation.objects.filter(slug= employee_slug).last()
            if not employee_qs:
                return ResponseWrapper(error_msg='Employee is Not Found', error_code=404)
        
        qs = serializer.save(
                created_by=request.user,
                slug=slug,
                pos_area = pos_area_qs, 
            )
        
        if employee_qs:
            employee_qs.pos_area = qs
            employee_qs.save()
        
        serializer = POSRegionSerializer(instance=qs)
        
        return ResponseWrapper(data= serializer.data, msg='Success', status=200)    

    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        if request.data.get('employee_slug'):
            employee_slug = request.data.pop('employee_slug')
            
        employee_qs = None
        serializer = serializer_class(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        name = request.data.get('name')
        pos_area_qs = None
        
        qs = self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_msg="POS Region is Not Found", error_code=404)
        
        office_location_qs = self.queryset.exclude(slug = qs.slug).filter(slug = slug).last()
        
        if office_location_qs:
            return ResponseWrapper(error_msg="POS Region is Already Found", error_code=404)
        
        if request.data.get('pos_area'):
        
            pos_area_qs = POSRegion.objects.filter(slug = str(request.data.get('pos_area'))).last()
            if not pos_area_qs:
                return ResponseWrapper(error_msg='POS Area is Not Found', error_code=404)
            
            
            pos_area = serializer.validated_data.pop('pos_area', None)
            
        

        if employee_slug:
            employee_qs = EmployeeInformation.objects.filter(slug= employee_slug).last()
            if not employee_qs:
                return ResponseWrapper(error_msg='Employee is Not Found', error_code=404)
        
        qs = serializer.update(
            instance=qs, 
            validated_data=serializer.validated_data
            )
        
        qs.updated_by=request.user
        if pos_area_qs:
            qs.pos_area=pos_area_qs
        qs.save()
        
        if employee_qs:
            employee_qs.pos_reason = qs.last()
            employee_qs.save()
        
        serializer = POSRegionSerializer(instance=qs)
        return ResponseWrapper(data= serializer.data, msg='POS Region Updated', status=200)
