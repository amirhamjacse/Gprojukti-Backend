import random
from django.conf import settings
from gporjukti_backend_v2.settings import TODAY
from human_resource_management.filters import *
from utils.response_wrapper import ResponseWrapper

from django.db.models import Q

# User = get_user_model()
from utils.permissions import CheckCustomPermission
# import re
from human_resource_management.serializers.attendance import *
from human_resource_management.models.attendance import *
from utils.custom_veinlet import CustomViewSet
from utils.permissions import *
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from utils.decorators import log_activity

class EmployeeOfficeHourViewSet(CustomViewSet):
    queryset = EmployeeOfficeHour.objects.all()
    lookup_field = 'pk'
    serializer_class = EmployeeOfficeHourSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = EmployeeOfficeHourFilter
    
    def get_serializer_class(self):
        if self.action in ["create", 'update']:
            self.serializer_class = EmployeeOfficeHourCreateUpdateSerializer
        elif self.action in ["employee_office_hour"]:
            self.serializer_class = EmployeeOfficeHourCreateUpdateSerializer
        elif self.action in ["list"]:
            self.serializer_class = EmployeeOfficeHourListSerializer
        else:
            self.serializer_class = EmployeeOfficeHourSerializer

        return self.serializer_class
    
    @log_activity
    def employee_office_hour(self, request, employee_slug, *args, **kwargs):
        employee_qs = EmployeeInformation.objects.filter(slug = employee_slug).last()
        
        if not employee_qs:
            return ResponseWrapper(error_msg='Employee Information is Not Found', error_code=404)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, many=True)
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        office_hour_list = request.data
        for office_hour in office_hour_list:
            working_days = office_hour.get("day")
            start_time = office_hour.get("start_time")
            end_time = office_hour.get("end_time")
            grace_time = office_hour.get("grace_time")
            type = office_hour.get("type") or 'REGULAR'
            
            qs = EmployeeOfficeHour.objects.filter(day = working_days, employee_information = employee_qs)
            
            if not qs:
                qs = EmployeeOfficeHour.objects.create( 
                        employee_information = employee_qs, 
                        created_by=self.request.user,
                        start_time=start_time,
                        end_time=end_time,
                        grace_time=grace_time,
                        type=type,
                        day=working_days
                    )
            else:
                qs = qs.update(
                    start_time=start_time,
                    end_time=end_time,
                    grace_time=grace_time,
                    type=type,
                    day=working_days
                    )
                
        office_hour_qs = EmployeeOfficeHour.objects.filter(employee_information = employee_qs)
        
        serializer = EmployeeOfficeHourSerializer(office_hour_qs, many=True)
        return ResponseWrapper(data=serializer.data, msg='Success')
     
    
class EmployeeAttendanceViewSet(CustomViewSet):
    queryset = EmployeeAttendance.objects.all().exclude(employee_information__user__user_informations__user_type__name__icontains = "Shop User")
    lookup_field = 'slug'
    serializer_class = EmployeeAttendanceSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = EmployeeAttendanceFilter 
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = EmployeeAttendanceCreateSerializer
        elif self.action in ['update']:
            self.serializer_class = EmployeeAttendanceUpdateSerializer
        elif self.action in ['list']:
            self.serializer_class = EmployeeAttendanceListSerializer
        else:
            self.serializer_class = EmployeeAttendanceSerializer

        return self.serializer_class
    
    @log_activity
    def list(self, request, *args, **kwargs):
        qs = (
            self.filter_queryset(self.get_queryset())
            .exclude(employee_information__user__user_informations__user_type__name='Shop')
        )

        
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

    
    @log_activity
    def employee_attendance_overview_list(self, request, *args, **kwargs):
        context = [
            {
                'msg': "Today's Head Office Attendance",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Today's Warehouse Attendance",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Today's Head Office Late Attendance",
                'quantity': random.randint(333, 7342),
                'ratio': f"-{random.randint(21, 99)}%",
            },
            {
                'msg': "Today's Warehouse Late Attendance",
                'quantity': random.randint(333, 7342),
                'ratio': f"-{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    @log_activity
    def create(self, request, employee_slug, *args, **kwargs):
        employee_qs = EmployeeInformation.objects.filter(slug = employee_slug).last()
        
        if not employee_qs:
            return ResponseWrapper(error_msg='Employee Information is Not Found', error_code=404)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        
        employee_office_hour_qs = None

        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

        validated_data = serializer.validated_data
        working_date = validated_data.pop('working_date', None)
        working_description = validated_data.pop('working_description', None)

        if not working_date:
            working_date = TODAY
            
        
        day = working_date.strftime("%A").upper()
        
        employee_office_hour_qs = EmployeeOfficeHour.objects.filter(employee_information__slug = employee_slug, day = day).last()

        employee_attendance_qs = EmployeeAttendance.objects.filter(employee_information=employee_qs, working_date__date = working_date.date()).last()
        
        print('ggggggggg', employee_attendance_qs)

        status = 'APPROVED'
        attendance_type = 'ON_TIME'
        office_hour_type = "Regular"
        
        if employee_office_hour_qs:
            office_hour_type = employee_office_hour_qs.type
        
        if not working_date.date() == TODAY.date():
            status = 'INITIALIZED'
            
        if not employee_attendance_qs:
            qs = serializer.save(
                employee_office_hour=employee_office_hour_qs,
                # status=status,
                employee_information=employee_qs,
                office_hour_type=office_hour_type,
                created_by = request.user,
            )
            
            qs.check_out = qs.working_date
            
            if employee_office_hour_qs:
                qs.attendance_type = office_hour_type
                
            if qs.check_in and qs.check_out:
                
                duration = qs.check_in - qs.check_out
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                total_office_hour = f"{duration.days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds"
                qs.total_office_hour = total_office_hour
            
            qs.save()
            
            
        if employee_attendance_qs:
            employee_attendance_qs.check_out = working_date
            employee_attendance_qs.check_out = working_date
            employee_attendance_qs.status = status
            employee_attendance_qs.working_description = working_description
            employee_attendance_qs.employee_information=employee_qs
            employee_attendance_qs.save()
            
            qs = employee_attendance_qs
            
        employee_attendance_qs = EmployeeAttendance.objects.filter(employee_information=employee_qs, working_date__date = working_date.date()).last()
        
        serializer = EmployeeAttendanceSerializer(employee_attendance_qs)
            
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
