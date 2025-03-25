from django.db import models

from django.utils.translation import gettext_lazy as _
from human_resource_management.models.employee import EmployeeInformation
from user.models import UserAccount
from django.utils.timezone import timedelta

from django.utils.translation import gettext_lazy as _
from utils.helpers import (
    time_str_mix_slug)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from base.models import DAYS, Company
from location.models import Area
from utils.generates import unique_slug_generator

# Create your models here.

        
class EmployeeOfficeHour(models.Model):
    TYPE = [
        ("REGULAR","Regular"),
        ("EXTRA","Extra"),
        ("SPECIAL","SPECIAL")
    ]
    employee_information = models.ManyToManyField(
        to=EmployeeInformation, blank=True, related_name='employee_office_hours')
    slug = models.CharField(max_length=250, blank=True, null=True)
    day = models.CharField(choices = DAYS, max_length=50,
                          blank=True, null = True)
    type = models.CharField(max_length=20, choices=TYPE, default="REGULAR")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    grace_time = models.TimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_office_hour_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_office_hour_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.employee_information:
            return f"Employee Name = {self.employee_information.name} and {self.get_day_display()}, Office Hour = {self.start_time} - {self.end_time}"
        return str(self.id)
                
class EmployeeAttendance(models.Model):
    ATTENDANCE_STATUS = [
        ("INITIALIZED", "Initialized"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]
    ATTENDANCE_TYPE = [
        ('ON_TIME', 'On Time'),
        ('OVER_TIME', 'Over Time'),
        ('LATE', 'Late'),
        ('ABSENT', 'Absent'),
        ('CASUAL_LEAVE', 'Casual Leave'),
        ('SICK_LEAVE', 'Sick Leave'),
        ('SPECIAL_LEAVE', 'Special Leave'),
        ('PATERNITY_LEAVE', 'Paternity Leave'),
        ('MATERNITY_LEAVE', 'Maternity Leave'),
        ('EXTRA_OFFICE_DAY', 'Extra Office Day'),
    ]
    employee_information = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_attendances')
    employee_office_hour = models.ForeignKey(
        EmployeeOfficeHour, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_attendances')
    slug = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default="APPROVED")
    attendance_type = models.CharField(max_length=20, choices=ATTENDANCE_TYPE, default="ON_TIME")
    working_description = models.TextField(blank=True, null=True)
    total_office_hour = models.CharField(max_length=20, blank=True, null=True)
    
    working_date = models.DateTimeField(blank=True, null=True)
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    office_hour_type = models.CharField(max_length=50,blank=True, null=True)
    approved_by = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_attendance_approved_bys')
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default = False)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_attendance_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_attendance_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.employee_office_hour:
            return str(self.employee_office_hour.employee_information.name)
        return str(self.id)
    
class EmployeeAttendanceLog(models.Model):
    employee_attendance = models.ForeignKey(
        EmployeeAttendance, on_delete=models.SET_NULL, blank=True, null=True,  related_name='employee_attendance_logs')
    working_description = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=50,blank=True, null=True)
    status_display = models.CharField(max_length=50,blank=True, null=True)
    working_date = models.DateTimeField(blank=True, null=True)
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    status_change_by_info = models.JSONField(blank=True, null=True)
    approved_by_info = models.JSONField(blank=True, null=True)
    reason = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default = False)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_attendance_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_attendance_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.employee_attendance)
