import random
from django.conf import settings
from base.models import UserNotification
from human_resource_management.filters import *
from human_resource_management.models.calender import EventOrNotice
from human_resource_management.serializers.dashboard import DashboardNoticeListSerializer
from order.models import Order
from user.models import UserInformation
from utils.base import get_user_store_list
from utils.decorators import log_activity
from utils.generates import generate_task_no
from utils.response_wrapper import ResponseWrapper

from django.db.models import Q

# User = get_user_model()
from utils.permissions import CheckCustomPermission
# import re
from human_resource_management.serializers.calender import *
from human_resource_management.models.calender import *
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from utils.permissions import *
from django.db import transaction
# Create your views here.
from rest_framework.generics import get_object_or_404  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from drf_extra_fields.fields import Base64FileField, Base64ImageField
from utils.actions import send_action, activity_log

from channels.layers import get_channel_layer

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

 
class EventTypeViewSet(CustomViewSet):
    queryset = EventType.objects.all()
    lookup_field = 'pk'
    serializer_class = EventTypeSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = None
    
    def get_permissions(self):
        if self.action in ["create",]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class EventOrNoticeViewSet(CustomViewSet):
    queryset = EventOrNotice.objects.all().order_by('-created_at')
    lookup_field = 'pk'
    serializer_class = EventOrNoticeSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = EventOrNoticeFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = EventOrNoticeCreateUpdateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = EventOrNoticeSerializer
        else:
            self.serializer_class = EventOrNoticeListSerializer

        return self.serializer_class
    
    def get_permissions(self):
        if self.action in ["create",]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

    
    @log_activity
    def notice_overview_list(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request_user = request.user)
         
        # notice_qs = EventOrNotice.objects.filter(Q(office_location__slug__in = shop_qs.values_list('slug', flat = True)) | Q(employee__work_station__slug__in = shop_qs.values_list('slug', flat = True)))
        notice_qs = EventOrNotice.objects.filter()
        
        context = [
            {
                'msg': "Total Notice",
                'quantity': notice_qs.count(),
                'ratio': f"100%",
            },
            {
                'msg': "Active Notice",
                'quantity': random.randint(2, 4),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Upcoming",
                'quantity': random.randint(3, 5),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Passed Notice",
                'quantity': random.randint(3, 4),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    @log_activity
    def event_overview_list(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request_user = request.user)
         
        # notice_qs = EventOrNotice.objects.filter(Q(office_location__slug__in = shop_qs.values_list('slug', flat = True)) | Q(employee__work_station__slug__in = shop_qs.values_list('slug', flat = True)))
        notice_qs = EventOrNotice.objects.filter()
        
        context = [
            {
                'msg': "Total Event",
                'quantity': notice_qs.count(),
                'ratio': f"100%",
            },
            {
                'msg': "Active Event",
                'quantity': random.randint(2, 4),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Upcoming",
                'quantity': random.randint(3, 5),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Passed Notice",
                'quantity': random.randint(3, 4),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    # ..........***.......... Create ..........***..........
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        name = ''
        
        if request.data.get('name'):
            name = request.data.get('name')
        elif request.data.get('title'):
            name = request.data.get('title')
        else:
            name = name
            
        try:
            qs = self.queryset.filter(name = request.data.get('name')) or self.queryset.filter(title = request.data.get('title'))
            
            if qs:
                return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
        except:
            pass
            
        if serializer.is_valid():
            is_add_in_calendar = serializer.validated_data.pop('is_add_in_calendar', None)
            is_occupied = serializer.validated_data.pop('is_occupied', None)
            
            if name:
                slug = unique_slug_generator(name = name) 
                
            serializer.validated_data['created_by'] = request.user
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

            activity_log(qs, request,serializer)

            try:
                employee_list = qs.employee.all()
                print('employee_list', employee_list)
                
                for employee in employee_list:
                    employee_user = employee.user
                    channel_layer = get_channel_layer()
                    
                    group_name = f'admin-panel-{employee_user.id}'
                    
                    try:
                        async_to_sync(channel_layer.group_send)(
                            group_name,
                            {
                                'type': 'send_notification',
                                'data': f"{qs.name} Has Been Created"
                            }
                        )
                        logger.info(f'Notification sent for user {employee_user.id} with order data: {qs.name} Has Been Created')
                        print('Success')
                    except Exception as send_error:
                        logger.error(f'Error sending WebSocket notification to user {employee_user.id}: {send_error}')
                    
                    try:
                        time_str = f'{(qs.created_at+timedelta(hours=6)).strftime("%d %B, %Y at %I:%M %p")}'
                        
                        
                        description = f"A <b>{qs.get_type_display()}</b> which is <b>'{qs.name}'</b> Has Been Created For <b>'{employee.name}'</b> at <b>{time_str}</b>"
                        
                        UserNotification.objects.create(
                            title=f"{qs.name} Has Been Created",
                            created_by=request.user,
                            user_information=employee_user,
                            description=description
                        )
                        
                    except Exception as notification_error:
                        logger.error(f'Error creating notification for user {employee_user.id}: {notification_error}')
                        
                print('employee_list', employee_list)
                
                office_employee_list = EmployeeInformation.objects.filter(work_station__slug__in= qs.office_location.values_list('slug', flat= True))
                
                for employee in office_employee_list:
                    employee_user = employee.user
                    channel_layer = get_channel_layer()
                    
                    group_name = f'admin-panel-{employee_user.id}'
                    
                    try:
                        async_to_sync(channel_layer.group_send)(
                            group_name,
                            {
                                'type': 'send_notification',
                                'data': f"{qs.name} Has Been Created"
                            }
                        )
                        logger.info(f'Notification sent for user {employee_user.id} with order data: {qs.name} Has Been Created')
                        print('Success')
                    except Exception as send_error:
                        logger.error(f'Error sending WebSocket notification to user {employee_user.id}: {send_error}')
                    
                    try:
                        time_str = f'{(qs.created_at+timedelta(hours=6)).strftime("%d %B, %Y at %I:%M %p")}'
                        
                        
                        description = f"A <b>{qs.get_type_display()}</b> which is <b>'{qs.name}'</b> Has Been Created For <b>'{employee.name}'</b> at <b>{time_str}</b>"
                        
                        UserNotification.objects.create(
                            title=f"{qs.name} Has Been Created",
                            created_by=request.user,
                            user_information=employee_user,
                            description=description
                        )
                        
                    except Exception as notification_error:
                        logger.error(f'Error creating notification for user {employee_user.id}: {notification_error}')

            except Exception as e:
                logger.error(f'Error processing employee notifications: {e}')

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

class EmployeeCalendarViewSet(CustomViewSet):
    queryset = EmployeeCalendar.objects.all()
    lookup_field = 'pk'
    serializer_class = EmployeeCalendarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = EmployeeCalendarCreateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = EmployeeCalendarSerializer
        else:
            self.serializer_class = EmployeeCalendarSerializer

        return self.serializer_class
    
    
class EmployeeTaskViewSet(CustomViewSet):
    queryset = EmployeeTask.objects.all()
    lookup_field = 'pk'
    serializer_class = EmployeeTaskListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = EmployeeTaskFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = EmployeeTaskCreateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = EmployeeTaskDetailsSerializer
        else:
            self.serializer_class = EmployeeTaskListSerializer

        return self.serializer_class
    
    # def get_permissions(self):
    #     if self.action in ["create",]:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
    
    
    # ..........***.......... Create ..........***..........
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        name = ''
        
        if request.data.get('name'):
            name = request.data.get('name')
            
        qs = self.queryset.filter(name = request.data.get('name')) 
        if qs:
            return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
            
        if serializer.is_valid():
            is_add_in_calendar = serializer.validated_data.pop('is_add_in_calendar', None)
            is_occupied = serializer.validated_data.pop('is_occupied', None)
            
            employee_qs = None
            
            slug = unique_slug_generator(name = name) 
                
            serializer.validated_data['created_by'] = request.user
            
            try:
                serializer.validated_data['slug'] = slug
            except:
                pass
            
            employee = request.data.get('employee')
            
            if not employee:
                return ResponseWrapper(error_msg=" Employee Information is Mandatory")
            employee_qs = EmployeeInformation.objects.filter(slug = employee).last()
            
            serializer.validated_data['employee'] = employee_qs
            
            last_task_no = 'TASK000-1'
            
            task_qs = EmployeeTask.objects.all().order_by('id').last()
            if task_qs:
                if task_qs.task_no:
                    last_task_no = task_qs.task_no
                
            serializer.validated_data['task_no'] = generate_task_no(last_task_no)
            
            try:
                qs = serializer.save()
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()
            
            try:
                if employee_qs:
                    group_name = f'admin-panel-{employee_qs.user.id}'
                    channel_layer = get_channel_layer()
                    
                    try:
                        async_to_sync(channel_layer.group_send)(
                            group_name,
                            {
                                'type': 'send_notification',
                                'data': f"{qs.name} Has Been Created"
                            }
                        )
                        logger.info(f'Notification sent for user {employee_qs.user.id} with order data: {qs.name} Has Been Created')
                        
                        print('Success')
                        
                    except Exception as send_error:
                        logger.error(f'Error sending WebSocket notification to user {employee_qs.user.id}: {send_error}')
                
                    try:
                        time_str = f'{(qs.created_at+timedelta(hours=6)).strftime("%d %B, %Y at %I:%M %p")}'
                        
                        
                        description = f"A <b>#{qs.task_no}</b>, Which is <b>'{qs.name}'</b> Has Been Created For <b>'{employee_qs.name}'</b> at <b>{time_str}</b>"
                        
                        UserNotification.objects.create(
                            title=f"The Task '{qs.name}' Has Been Created",
                            created_by=request.user,
                            user_information=employee_qs.user,
                            description=description
                        )
                        
                    except Exception as e:
                        logger.error(f'Error processing employee notifications: {e}')
                        
            except Exception as e:
                logger.error(f'Error processing employee notifications: {e}')
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
