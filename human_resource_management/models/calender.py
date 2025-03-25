from django.db import models

# from base.models import CALENDER_TYPE
from human_resource_management.models.employee import EmployeeInformation
from location.models import OfficeLocation
from user.models import UserAccount


CALENDER_TYPE = [
    ("BUSY", 'Busy'),
    ("FREE", 'Free'),
]

TASK_STATUS = [
    ("PENDING", 'Pending'),
    ("IN_PROGRESS", 'In Progress'),
    ("FEEDBACK", 'Feedback'),
    ("REJECT", 'Reject'),
    ("PAUSED", 'Paused'),
    ("DONE", 'Done'),
]

class EventType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='event_type_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='event_type_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name 
    
class EventOrNotice(models.Model):
    TYPE = [
        ("NOTICE", 'Notice'),
        ("EVENT", 'Event'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    event_url = models.TextField(blank=True, null=True)
    employee = models.ManyToManyField(
        to=EmployeeInformation,blank=True,
        related_name='event_or_notices'
        )
    office_location = models.ManyToManyField(
        to=OfficeLocation,blank=True,
        related_name='event_or_notices'
        )
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,blank=True, null = True,
        related_name='event_or_notices')
    
    type = models.CharField(max_length=50, 
                            choices=TYPE, default="EVENT")
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='event_or_notice_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='event_or_notice_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name 

class EmployeeTask(models.Model):
    task_no = models.CharField(max_length=150, unique = True)
    employee = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL,blank=True, null = True,
        related_name='employee_tasks')
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, 
                            choices=TASK_STATUS, default="PENDING")
    approved_by = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL,blank=True, null = True,
        related_name='approved_by_employee_tasks')
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_task_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_task_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name
    
class EmployeeTaskStatusLog(models.Model):
    employee_task = models.ForeignKey(
        EmployeeTask, on_delete=models.SET_NULL ,null=True, blank=True,related_name='employee_task_status_logs')
    status = models.CharField(max_length=150)
    status_display = models.CharField(max_length=150)
    status_reason = models.TextField(null=True, blank=True)
    status_change_by = models.JSONField(blank=True, null=True)
    status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_task_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_task_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.employee_task.task_no)
    
class EmployeeCalendar(models.Model):
    employee = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL,blank=True, null = True,
        related_name='employee_calendars')
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,blank=True, null = True,
        related_name='employee_calendars')
    calender_type = models.CharField(max_length=50, 
                            choices=CALENDER_TYPE, default="FREE")
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='employee_calendar_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='employee_calendar_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name