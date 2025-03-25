from django.urls import path, include
from utils.upload_image import image_upload

from human_resource_management.views.admin.attendance import *

urlpatterns = [
     path('employee_office_hour/',
          EmployeeOfficeHourViewSet.as_view({'get': 'list', 'post':'create'},  name='employee_office_hour')),
     
     path('employee_office_hour/<id>/',
          EmployeeOfficeHourViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='employee_office_hour')),
     
     path('employee_daily_work/<employee_slug>/',
          EmployeeAttendanceViewSet.as_view({'post': 'create'},  name='employee_daily_work')),
     
     path('employee_attendance/',
          EmployeeAttendanceViewSet.as_view({'get': 'list'},  name='employee_attendance')),
     path('employee_attendance/<slug>/',
          EmployeeAttendanceViewSet.as_view({'get': 'retrieve', 'patch': 'update'},  name='employee_attendance')),
     path('employee_attendance_overview_list/',
          EmployeeAttendanceViewSet.as_view({'get': 'employee_attendance_overview_list'},  name='employee_attendance_overview_list')),
     
]