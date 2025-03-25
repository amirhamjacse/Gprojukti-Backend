from django.conf import settings
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer

from human_resource_management.models.employee import EmployeeInformation
from location.models import *
from user.serializers import BaseSerializer, BaseSerializer

class CountrySerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    slug = serializers.CharField(read_only = True)

    class Meta:
        model = Country
        fields = "__all__"

class DivisionSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    slug = serializers.CharField(read_only = True)
    district_count = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Division
        fields = "__all__"

    def get_district_count(self, obj):
        district_count = 0
        if obj.districts:
            district_count = obj.districts.count()
        return district_count
    
class DistrictSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    slug = serializers.CharField(read_only = True)

    class Meta:
        model = District
        fields = "__all__"
        
    
class PublicDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'id',
            'name',
            'slug',
            'bn_name',
        ]
        


class AreaSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    slug = serializers.CharField(read_only = True)

    class Meta:
        model = Area
        fields = "__all__"

class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
                'id',  
                'name',  
                'slug',  
                'bn_name',  
                ]


class OfficeLocationListSerializer(serializers.ModelSerializer): 
    slug = serializers.CharField(read_only = True)
    office_type_display = serializers.CharField(source='get_office_type_display')
    area = AreaListSerializer(read_only=True)

    class Meta:
        model = OfficeLocation
        fields = [
            'id',
            'name',
            'slug',
            'area',
            'office_type',
            'office_type_display',
            'primary_phone',
            'store_no',
            'email',
            'pos_area_name',
            'pos_region_name',
            'is_use_scanner',
                  ]

class OfficeLocationLiteSerializer(serializers.ModelSerializer): 
    class Meta:
        model = OfficeLocation
        fields = [
            'id',
            'name',
            'slug'
                  ]

class OfficeLocationCreateUpdateSerializer(serializers.ModelSerializer):
    area = serializers.CharField()
    class Meta:
        model = OfficeLocation
        fields = [
            'id',
            'name',
            'bn_name',
            'address',
            'primary_phone',
            'email', 
            'map_link',
            'opening_time',
            'closing_time',
            'area',
            'office_type',
            'is_shown_in_website',
            'is_active',
            'is_shown_in_website',
            'off_days',
        ]
        
        
    
class POSAreaListSerializer(serializers.ModelSerializer):
    area = AreaListSerializer(read_only=True)
    
    class Meta:
        model = POSArea
        fields = [
                'id',  
                'name',  
                'slug',  
                'bn_name',  
                'is_active',  
                'area',  
                ]  
        
class POSAreaSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    area = AreaListSerializer(read_only=True)
    employee_information = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = POSArea
        fields = "__all__"  
        
    def get_employee_information(self, obj):
        employee_id = None
        employee_name = None
        employee_slug = None
        employee_image = settings.NOT_FOUND_IMAGE
        
        employee_qs = EmployeeInformation.objects.filter(pos_area = obj).last()
        if employee_qs:
            employee_id =  employee_qs.employee_id
            employee_name =  employee_qs.name
            employee_slug =  employee_qs.slug
            employee_image =  employee_qs.image
        
        context = {
            'id': employee_id,
            'name': employee_name,
            'slug': employee_slug,
            'image': employee_image,
        }
        return context
        
class POSAreaCreateSerializer(serializers.ModelSerializer):
    area = serializers.CharField(read_only=True)
    employee_slug = serializers.CharField(read_only=True)
    
    class Meta:
        model = POSArea
        fields = [
            'id',
            'name',                
            'bn_name',                 
            'area',        
            'employee_slug',        
            'is_active',        
            'remarks',        
                ]        
        
class POSRegionListSerializer(serializers.ModelSerializer):
    pos_area = POSAreaListSerializer(read_only=True, many=True)
    
    class Meta:
        model = POSRegion
        fields = [
                'id',  
                'name',  
                'slug',  
                'bn_name',  
                'is_active',  
                'pos_area',  
                ]  
        
class POSRegionSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    pos_area = POSAreaListSerializer(read_only=True)
    employee_information = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = POSRegion
        fields = "__all__"  
        
    def get_employee_information(self, obj):
        employee_id = None
        employee_name = None
        employee_slug = None
        employee_image = settings.NOT_FOUND_IMAGE
        
        employee_qs = EmployeeInformation.objects.filter(pos_reason = obj).last()
        if employee_qs:
            employee_id =  employee_qs.employee_id
            employee_name =  employee_qs.name
            employee_slug =  employee_qs.slug
            employee_image =  employee_qs.image
        
        context = {
            'id': employee_id,
            'name': employee_name,
            'slug': employee_slug,
            'image': employee_image,
        }
        return context
        
class POSRegionCreateSerializer(serializers.ModelSerializer):
    pos_area = serializers.CharField(read_only=True)
    employee_slug = serializers.CharField(read_only=True)
    
    class Meta:
        model = POSRegion
        fields = [
            'id',
            'name',                
            'bn_name',                 
            'pos_area',        
            'employee_slug',        
            'is_active',        
            'remarks',        
                ]        
    
class OfficeLocationSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    company = CompanyLiteSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    
    class Meta:
        model = OfficeLocation
        fields = "__all__"
        
        
class DistrictWiseShopSerializer(serializers.ModelSerializer):
    shop_list = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = District
        fields = "__all__"
        
    def get_shop_list(self, obj):
        shop_qs = OfficeLocation.objects.filter(office_type = "STORE", is_active = True , area__in = obj.areas.all()) 
        serializer = OfficeLocationSerializer(instance=shop_qs, many= True)
        return serializer.data  
        
        
class AreaWiseShopSerializer(serializers.ModelSerializer):
    shop_list = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Area
        fields = [
                'id',  
                'name',  
                'bn_name',  
                'slug',  
                'shop_list',  
                ]
        
    def get_shop_list(self, obj):
        shop_qs = OfficeLocation.objects.filter(office_type = "STORE", is_active = True , area = obj) 
        serializer = OfficeLocationListSerializer(instance=shop_qs, many= True)
        return serializer.data 