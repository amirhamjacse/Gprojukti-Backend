from courier_management.filters import CourierServiceFilter, DeliveryManFilter
from courier_management.models import *
from courier_management.serializers import *
from utils.actions import activity_log
from utils.custom_veinlet import CustomViewSet
from utils.generates import unique_slug_generator
from utils.permissions import CheckCustomPermission
from utils.response_wrapper import ResponseWrapper
from django.utils import timezone
from order.filters import *
from utils.decorators import log_activity

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

class CourierServiceViewSet(CustomViewSet):
    queryset = CourierService.objects.all()
    lookup_field = 'slug'
    serializer_class = CourierServiceListSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CourierServiceFilter
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = CourierServiceSerializer
        elif self.action in ['list']:
            self.serializer_class = CourierServiceListSerializer
        else:
            self.serializer_class = CourierServiceSerializer
            
        return self.serializer_class

class DeliveryManViewSet(CustomViewSet):
    queryset = DeliveryMan.objects.all()
    lookup_field = 'slug'
    serializer_class = DeliveryManListSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DeliveryManFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = DeliveryManCreateUpdateSerializer
        elif self.action in ['list']:
            self.serializer_class = DeliveryManListSerializer
        else:
            self.serializer_class = DeliveryManSerializer
            
        return self.serializer_class
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        name = ''
        
        name = request.data.get('name')
             
        qs = self.queryset.filter(name = request.data.get('name'))
        
        if qs:
            return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
             
        employee_qs = EmployeeInformation.objects.filter(slug = request.data.get('employee')).last()
        
        if not employee_qs:
            return ResponseWrapper(error_msg="Employee Information is Not Found", error_code=404)
             
        courier_service_qs = CourierService.objects.filter(slug = request.data.get('courier_service')).last()
        
        if not courier_service_qs:
            return ResponseWrapper(error_msg="Courier Service is Not Found", error_code=404)
        
        if serializer.is_valid():
            if name:
                slug = unique_slug_generator(name = name) 
                
            serializer.validated_data['created_by'] = request.user
            serializer.validated_data['employee'] = employee_qs
            serializer.validated_data['courier_service'] = courier_service_qs
            
            try:
                serializer.validated_data['slug'] = slug
            except:
                pass
            
            try:
                qs = serializer.save()
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()
                
            serializer = DeliveryManSerializer(qs)

            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        delivery_man_qs = self.queryset.filter(slug = slug).last()
        if not delivery_man_qs: 
            return ResponseWrapper(error_msg="Delivery Man Information is Not Found", error_code=404)
        
        if request.data.get('name'):
            qs = self.queryset.exclude(slug = delivery_man_qs).filter(name = request.data.get('name'))
            if qs:
                return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
             
        employee_qs = delivery_man_qs.employee
        courier_service_qs = delivery_man_qs.courier_service
        
        if request.data.get('employee'):
            employee_qs = EmployeeInformation.objects.filter(slug = request.data.get('employee')).last()          
        
            if not employee_qs:
                return ResponseWrapper(error_msg="Employee Information is Not Found", error_code=404)
             
        if request.data.get('courier_service'):
            courier_service_qs = CourierService.objects.filter(slug = request.data.get('courier_service')).last()
        
            if not courier_service_qs:
                return ResponseWrapper(error_msg="Courier Service is Not Found", error_code=404)
        
        if serializer.is_valid(): 
            serializer.validated_data['updated_by'] = request.user
            serializer.validated_data['employee'] = employee_qs
            serializer.validated_data['courier_service'] = courier_service_qs
            
            qs = serializer.update(instance=delivery_man_qs, validated_data=serializer.validated_data)
            try:
                if qs:
                    qs.updated_by_id = self.request.user.id
                    qs.save()
            except:
                qs = qs

            serializer = DeliveryManSerializer(instance=qs)
            
            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='Updated', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
