from rest_framework import serializers
from base.serializers import EmployeeInformationBaseSerializer, UserInformationBaseSerializer
from gporjukti_backend_v2 import settings
from human_resource_management.models.attendance import *
from human_resource_management.models.calender import *
from human_resource_management.serializers.employee import EmployeeInformationListSerializer
from location.serializers import OfficeLocationListSerializer
from user.serializers import BaseSerializer

class EventTypeSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only = True)
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    
    class Meta:
        model = EventType
        fields = "__all__"
        
        
class EventOrNoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrNotice
        fields = [
                'id',  
                'name',  
                'slug',  
                'color',  
                'start_date',  
                'end_date',  
                ]
        
class EventOrNoticeSerializer(serializers.ModelSerializer):
    event_type = serializers.CharField(write_only = True)
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    event_type = EventTypeSerializer(read_only = True)
    employee = EmployeeInformationListSerializer(many = True)
    office_location = OfficeLocationListSerializer(many = True)
    
    class Meta:
        model = EventOrNotice
        fields = "__all__"
        
class EventOrNoticeCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only = True)
    is_add_in_calendar = serializers.BooleanField(write_only = True)
    is_occupied = serializers.BooleanField(write_only = True)
    
    class Meta:
        model = EventOrNotice
        fields = [
                'name',
                'slug', 
                'color', 
                'description',
                'start_date',
                'end_date',
                'event_url',
                'employee',
                'office_location',
                'event_type',
                'type',
                'is_active',
                'is_add_in_calendar',
                'is_occupied',
                'remarks',
                ]
        
    def to_representation(self, instance):
        self.fields["event_type"] = EventTypeSerializer(read_only=True)
        return super(EventOrNoticeCreateUpdateSerializer, self).to_representation(instance)
    
    

class EmployeeCalendarSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only = True)
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    employee = EmployeeInformationListSerializer(read_only = True)
    event_type = EventTypeSerializer(read_only = True)
    calender_type_display = serializers.CharField(source = 'get_calender_type_display')
    
    class Meta:
        model = EmployeeCalendar
        fields = "__all__"
class EmployeeCalendarCreateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only = True)
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    class Meta:
        model = EmployeeCalendar
        fields = "__all__"
        
class EmployeeTaskListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source = 'get_status_display')
    employee_image = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = EmployeeTask
        fields = [
            'task_no',
            'name',
            'slug',
            'employee_image',
            'start_date',
            'end_date',
            'status',
            'status_display',
        ]
    def get_employee_image(self, obj):
        image = settings.NOT_FOUND_IMAGE
        return image
        

class EmployeeTaskDetailsSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    class Meta:
        model = EmployeeTask
        fields = "__all__"
        
class EmployeeTaskCreateSerializer(serializers.ModelSerializer): 
    employee = serializers.CharField(write_only = True) 
    class Meta:
        model = EmployeeTask
        fields = [
                "name",  
                "description",  
                "employee",  
                "start_date",  
                "end_date",  
                "is_active",  
                "remarks",  
                ]