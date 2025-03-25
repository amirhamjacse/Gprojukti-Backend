from rest_framework import serializers
from base.serializers import EmployeeInformationBaseSerializer, UserInformationBaseSerializer
from gporjukti_backend_v2 import settings
from human_resource_management.models.attendance import *

class EmployeeOfficeHourCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmployeeOfficeHour
        fields = [
                   'id',
                   'day',
                   'start_time',
                   'end_time',
                   'grace_time',
                   'type',
                   'employee_information',
                ]
class EmployeeOfficeHourListSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only = True)
    type_display = serializers.CharField(source='get_type_display', read_only = True)
    employee_information = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = EmployeeOfficeHour
        fields = [
                   'id',
                   'day',
                   'day_display',
                   'type',
                   'type_display',
                   'start_time',
                   'end_time',
                   'grace_time', 
                   'employee_information', 
                ]
        
    def get_employee_information(self, obj):
        employee_information = []
        if obj.employee_information.all():
            employee_information = obj.employee_information.values('image', 'name')[:5]
        
        return employee_information
        
class EmployeeOfficeHourSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only = True)
    employee_information = EmployeeInformationBaseSerializer(read_only = True, many = True)
    
    class Meta:
        model = EmployeeOfficeHour
        fields = '__all__'

class EmployeeAttendanceCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmployeeAttendance
        fields = [
                    'id',  
                    'working_date',  
                    'working_description',  
                ]
class EmployeeAttendanceUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmployeeAttendance
        fields = [
                    'id',  
                    'status',
                    'remarks',
                ]

class EmployeeAttendanceListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    attendance_type_display = serializers.CharField(source='get_attendance_type_display')
    employee_information = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = EmployeeAttendance
        fields = [
                  'id',
                  'slug',
                  'status_display',
                  'attendance_type_display',
                  'employee_information',
                  'check_in',
                  'check_out',
                ]
        
    def get_employee_information(self, obj):
        id = None
        employee_id = None
        name = "Jeba Fawjia"
        slug = None
        image = None
        image_url = 'https://i.pinimg.com/736x/3e/a9/47/3ea947c7c2ae57d763a9442fee8f1f2a.jpg'
        
        employee_qs = EmployeeInformation.objects.filter(user = obj.created_by).last()
         
        if employee_qs:
            id = employee_qs.id
            employee_id = employee_qs.employee_id
            
            if employee_qs.name or not employee_qs.name == " ":
                name = employee_qs.name
                
            slug = employee_qs.slug
            
            if employee_qs.image:
                image_url = employee_qs.image
            
        context = {
            'id':id,
            'employee_id':employee_id,
            'name':name,
            'slug':slug,
            'image':image_url,
        }
        return context
        
class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    attendance_type_display = serializers.CharField(source='get_attendance_type_display')
    
    # employee_office_hour = EmployeeOfficeHourSerializer()
    employee_information = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = EmployeeAttendance
        fields = '__all__'
        
    def get_employee_information(self, obj):
        context = {}
        image = settings.NOT_FOUND_IMAGE
        
        if obj.employee_information:
            employee_qs = EmployeeInformation.objects.filter(slug = obj.employee_information.slug).last()
        
            id = employee_qs.id
            employee_id =  employee_qs.employee_id
            name = employee_qs.name
            phone = employee_qs.user.phone
            email = employee_qs.user.email
            slug = employee_qs.slug
            if employee_qs.image:
                image = employee_qs.image
            
            designation_name = 'Sr. Software Engineer'
            work_station = 'GPrpojukti Head Office'
        
            context = {
                'id':id,
                'employee_id':employee_id,
                'name':name,
                'slug':slug,
                'image':image,
                'phone':phone,
                'email':email,
                'designation_name':designation_name,
                'work_station':work_station,
            }
        return context
        