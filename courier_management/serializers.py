from datetime import timedelta
from django.conf import settings
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer
from gporjukti_backend_v2.settings import TODAY
from courier_management.models import *
from django.db.models import Q


from human_resource_management.serializers.employee import EmployeeInformationListSerializer
from user.serializers import BaseSerializer
from django.utils import timezone

class CourierServiceListSerializer(serializers.ModelSerializer):
    courier_type_display = serializers.CharField(source='get_courier_type_display', read_only =  True)
    
    class Meta:
        model = CourierService
        fields = [
            'id',
            'name',
            'slug',
            'email',
            'phone',
            'courier_type',
            'courier_type_display',
                  ]

class CourierServiceSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only =  True)
    updated_by = BaseSerializer(read_only =  True)
    company = CompanyLiteSerializer(read_only =  True)
    courier_type_display = serializers.CharField(source='get_courier_type_display', read_only =  True)
    slug = serializers.CharField(read_only =  True)
    
    class Meta:
        model = CourierService
        fields = "__all__"

class DeliveryManListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = DeliveryMan
        fields = [
                  'id',
                  'name',
                  'slug',
                  'email',
                  'phone',
                  'image',
                ]
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        
        if obj.image:
            image_url = obj.image 
        return image_url

class DeliveryManCreateUpdateSerializer(serializers.ModelSerializer):
    employee = serializers.CharField()
    courier_service = serializers.CharField()
    
    class Meta:
        model = DeliveryMan
        fields = [
                  'id',
                  'name',
                  'email',
                  'phone',
                  'courier_service',
                  'employee',
                  'is_active',
                  'remarks',
                ]

class DeliveryManSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    courier_service = CourierServiceListSerializer(read_only = True)
    employee = EmployeeInformationListSerializer(read_only = True)
    slug = serializers.CharField(read_only = True)
    
    class Meta:
        model = DeliveryMan
        fields = "__all__"