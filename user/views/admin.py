from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import *
from utils.generates import unique_slug_generator
from utils.response_wrapper import ResponseWrapper

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

# import re
from user.models import *
from user.serializers import *
from user.filters import *

from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from utils.send_sms import otp_send_sms, send_email
import random
from django.contrib.auth.hashers import make_password
from utils.permissions import *
from rest_framework import permissions, status
from django.apps import apps
import re
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from utils.actions import send_action, activity_log
from utils.decorators import log_activity

import asyncio
import io
import openpyxl

from django.core.paginator import Paginator
import pandas as pd

from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.response import Response
from tablib import Dataset
from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from dateutil.relativedelta import relativedelta

@log_activity
def handle_permission(codename, name, model_class_name, serial_no):
    permission_qs = CustomPermission.objects.filter(codename=codename).last()
    if not permission_qs:
        CustomPermission.objects.create(
            name=name,
            codename=codename,
            model_name=model_class_name,
            serial_no=serial_no,
            is_active=True
        )
    else:
        CustomPermission.objects.filter(codename=codename).update(
            name=name,
            codename=codename,
            model_name=model_class_name,
            serial_no=serial_no,
            is_active=True
        )
        
        
class CustomPermissionViewSet(CustomViewSet):
    queryset = CustomPermission.objects.all().order_by('model_name')
    lookup_field = 'pk'
    serializer_class = CustomPermissionSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CustomPermissionFilter
    
    @log_activity
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer = CustomPermissionSerializer(qs, many=True)
        return ResponseWrapper(data=serializer.data, msg="Success", status=200)
    
    @log_activity
    def create(self, request, *args, **kwargs):
        all_models = {}
        count= 1

        # Get all installed apps
        for app_config in apps.get_app_configs():
            app_name = app_config.name

            # Check if the app belongs to the LOCAL_APPS
            if app_name in settings.LOCAL_APPS:
                models = [] 

                # Get models for the app
                for model in app_config.get_models():
                    models.append(model.__name__)

                all_models[app_name] = models
                
        for app_name, model_class_name_list in all_models.items():
            print(f"Row Number = {count}")
            for model_class_name in model_class_name_list:
                if model_class_name in ['BaseModel', 'CustomPermission']:
                    pass
                
                elif 'log' in model_class_name:
                    print(f"Pass Name = {model_class_name}")
                    pass
                    
                elif model_class_name in ['ProductStock']:
                    menu_code_permission = f"can_view_inventory_menu"
                    barcode_menu_code_permission = f"can_view_list_product_stock_barcode_menu"
                    multiple_barcode_print_code_permission = f"can_multiple_barcode_print"
                    single_barcode_print_code_permission = f"can_single_barcode_print"
                    multiple_same_barcode_print_code_permission = f"can_same_multiple_barcode_print"
                    same_barcode_print_code_permission = f"can_print_same_single_barcode" 
                    
                    # Permission Name
                    
                    menu_code_permission_name = f"Can View Inventory Menu"
                    barcode_menu_code_permission_name = f"Can View List Product Stock Barcode Menu"
                    multiple_barcode_print_code_permission_name = f"Can Multiple Barcode Print"
                    single_barcode_print_code_permission_name = f"Can Single Barcode Print"
                    multiple_same_barcode_print_code_permission_name = f"Can Same Multiple Barcode Print"
                    same_barcode_print_code_permission_name = f"Can Print Same Single Barcode" 

                    
                    
                    model_class_name = model_class_name  # Replace with your actual model class name
                    serial_no = '1'  # Replace with the actual serial number if needed

                    # Handle permissions
                    handle_permission(menu_code_permission, menu_code_permission_name, model_class_name, serial_no)
                    handle_permission(barcode_menu_code_permission, barcode_menu_code_permission_name, model_class_name, serial_no)
                    handle_permission(multiple_barcode_print_code_permission, multiple_barcode_print_code_permission_name, model_class_name, serial_no)
                    handle_permission(single_barcode_print_code_permission, single_barcode_print_code_permission_name, model_class_name, serial_no)
                    handle_permission(multiple_same_barcode_print_code_permission, multiple_same_barcode_print_code_permission_name, model_class_name, serial_no)
                    handle_permission(same_barcode_print_code_permission, same_barcode_print_code_permission_name, model_class_name, serial_no)
                    
                    print("Stock Permission Done")
                    
                elif model_class_name in ['Order', 'OrderHistoryLog']:
                    order_status_list = ORDER_STATUS
                    order_type_list = ORDER_TYPE
                    order_approved_status_list = ORDER_APPROVED_STATUS
                    
                    model_code_name  = ''.join(['_' + c.lower() if c.isupper() else c for c in model_class_name]).lstrip('_')
                    
                    class_name  = re.sub(r'(?<!^)(?=[A-Z])', ' ', model_class_name)
                    
                    count = 9
                    for status_code, status_name in order_status_list:
                        status_code = status_code.lower()
                        
                        code_permission = f"can_update_{model_code_name}_status_to_{status_code}"
                        
                        # Permission Name

                        display_permission = f"Can Update {class_name} Status To {status_name}"
                        
                        qs = CustomPermission.objects.filter(codename=code_permission)
                        
                        if not qs:
                            qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        else:
                            qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        count +=1
                        
                    count = count
                    
                    for order_type_code, order_type_name in order_type_list:
                        order_type_code = order_type_code.lower()
                        
                        # code_permission = f"can_create_{model_code_name}_{order_type_code}"
                        
                        list_code_permission = f"can_view_list_{model_code_name}_{order_type_code}"
                        add_code_permission = f"can_create_{model_code_name}_{order_type_code}"
                        update_code_permission = f"can_update_{model_code_name}_{order_type_code}"
                        destroy_code_permission = f"can_destroy_{model_code_name}_{order_type_code}"
                        retrieve_code_permission = f"can_retrieve_{model_code_name}_{order_type_code}"
                        menu_show_code_permission = f"can_show_{model_code_name}_{order_type_code}_menu"
                        download_code_permission = f"can_download_{model_code_name}_{order_type_code}"
                        upload_code_permission = f"can_upload_{model_code_name}_{order_type_code}"
                        
                        # Permission Name

                        # display_permission = f"Can Create {class_name} {order_type_name}"
                        
                        list_permission = f"Can View {class_name} {order_type_name}"
                        add_permission = f"Can Add {class_name} {order_type_name}"
                        update_permission = f"Can Update {class_name} {order_type_name}"
                        destroy_permission = f"Can Destroy {class_name} {order_type_name}"
                        retrieve_permission = f"Can Retrieve {class_name} {order_type_name}"
                        menu_show_permission = f"Can Show {class_name} {order_type_name} Menu"
                        download_permission = f"Can Download {class_name} {order_type_name}"
                        upload_permission = f"Can Upload {class_name} {order_type_name}"
                        
                        list_custom_permission_qs = CustomPermission.objects.filter(codename=list_code_permission)
                    
                        if not list_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = list_permission, codename = list_code_permission, model_name = model_class_name, serial_no = '1', is_active = True)
                        if list_custom_permission_qs:
                            qs = list_custom_permission_qs.update(name = list_permission, codename = list_code_permission, model_name = model_class_name, serial_no = '1', is_active = True)
                        
                        add_custom_permission_qs = CustomPermission.objects.filter(codename=add_code_permission)
                        
                        if not add_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = add_permission, codename = add_code_permission, model_name = model_class_name, serial_no = '2', is_active = True)
                        
                        if add_custom_permission_qs:
                            qs = add_custom_permission_qs.update(name = add_permission, codename = add_code_permission, model_name = model_class_name, serial_no = '2', is_active = True)
                        
                        update_custom_permission_qs = CustomPermission.objects.filter(codename=update_code_permission)
                        
                        if not update_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = update_permission, codename = update_code_permission, model_name = model_class_name, serial_no = '3', is_active = True)
                        if update_custom_permission_qs:
                            qs = update_custom_permission_qs.update(name = update_permission, codename = update_code_permission, model_name = model_class_name, serial_no = '3', is_active = True)
                        
                        retrieve_custom_permission_qs = CustomPermission.objects.filter(codename=retrieve_code_permission)
                        
                        if not retrieve_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = retrieve_permission, codename = retrieve_code_permission, model_name = model_class_name, serial_no = '4', is_active = True)
                            
                        if retrieve_custom_permission_qs:
                            qs = retrieve_custom_permission_qs.update(name = retrieve_permission, codename = retrieve_code_permission, model_name = model_class_name, serial_no = '4', is_active = True)
                        
                        destroy_custom_permission_qs = CustomPermission.objects.filter(codename=destroy_code_permission)
                        
                        if not destroy_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = destroy_permission, codename = destroy_code_permission, model_name = model_class_name, serial_no = '5', is_active = True)
                            
                        if destroy_custom_permission_qs:
                            qs = destroy_custom_permission_qs.update(name = destroy_permission, codename = destroy_code_permission, model_name = model_class_name, serial_no = '5', is_active = True)
                        
                        menu_show_custom_permission_qs = CustomPermission.objects.filter(codename=menu_show_code_permission)
                        
                        if not menu_show_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = menu_show_permission, codename = menu_show_code_permission, model_name = model_class_name, serial_no = '6', is_active = True)
                        
                        if menu_show_custom_permission_qs:
                            qs = menu_show_custom_permission_qs.update(name = menu_show_permission, codename = menu_show_code_permission, model_name = model_class_name, serial_no = '6', is_active = True)
                        
                        download_custom_permission_qs = CustomPermission.objects.filter(codename=download_code_permission)
                        
                        if not download_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = download_permission, codename = download_code_permission, model_name = model_class_name, serial_no = '7', is_active = True)
                            
                        if download_custom_permission_qs:
                            qs = download_custom_permission_qs.update(name = download_permission, codename = download_code_permission, model_name = model_class_name, serial_no = '7', is_active = True)
                        
                        upload_custom_permission_qs = CustomPermission.objects.filter(codename=upload_code_permission)
                        
                        if not upload_custom_permission_qs:
                            qs = CustomPermission.objects.create(name = upload_permission, codename = upload_code_permission, model_name = model_class_name, serial_no = '8', is_active = True)
                            
                        if upload_custom_permission_qs:
                            qs = upload_custom_permission_qs.update(name = upload_permission, codename = upload_code_permission, model_name = model_class_name, serial_no = '8', is_active = True)
                                
                        count +=1
                        
                    for order_approved_status_code, order_approved_status_name in order_approved_status_list:
                        order_approved_status_code = order_approved_status_code.lower()
                        
                        code_permission = f"can_create_{model_code_name}_{order_approved_status_code}"
                        
                        # Permission Name

                        display_permission = f"Can Create {class_name} {order_approved_status_name}"
                        
                        qs = CustomPermission.objects.filter(codename=code_permission)
                        
                        if not qs:
                            qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        else:
                            qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        count +=1
                    
                elif model_class_name in ['OrderItem']:
                    order_status_list = ORDER_ITEM_STATUS
                    
                    model_code_name  = ''.join(['_' + c.lower() if c.isupper() else c for c in model_class_name]).lstrip('_')
                    
                    class_name  = re.sub(r'(?<!^)(?=[A-Z])', ' ', model_class_name)
                    
                    count = 7
                    for status_code, status_name in order_status_list:
                        status_code = status_code.lower()
                        
                        code_permission = f"can_update_{model_code_name}_status_to_{status_code}"
                        
                        # Permission Name

                        display_permission = f"Can Update {class_name} Status To {status_name}"
                        
                        qs = CustomPermission.objects.filter(codename=code_permission)
                        
                        if not qs:
                            qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        else:
                            qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        count +=1
                    
                elif model_class_name in ['ProductStockTransfer']:
                    STOCK_TRANSFER_STATUS = [
                        ("IN_TRANSIT", 'In-Transit'),
                        ("NOT_UPDATED", 'Not Updated'),
                        ("UPDATED", 'Updated'),
                        ("APPROVED", 'Approved'),
                        ("FAILED", 'Failed'),
                        ("ON_HOLD", 'On Hold'),
                        ("CANCELLED", 'Cancelled'),
                    ]    
                    
                    STOCK_TRANSFER_TYPE = [
                        ("TRANSFER", 'Transfer'),
                        ("REQUISITION", 'Requisition'),
                    ]
                    
                    stock_transfer_status_list = STOCK_TRANSFER_STATUS
                    stock_transfer_type_list = STOCK_TRANSFER_TYPE
                    
                    model_code_name  = ''.join(['_' + c.lower() if c.isupper() else c for c in model_class_name]).lstrip('_')
                    
                    class_name  = re.sub(r'(?<!^)(?=[A-Z])', ' ', model_class_name)
                    
                    count = 7
                    for code, name in stock_transfer_status_list:
                        code = code.lower()
                        
                        code_permission = f"can_update_{model_code_name}_status_to_{code}"
                        
                        # Permission Name

                        display_permission = f"Can Update {class_name} Status To {name}"
                        
                        qs = CustomPermission.objects.filter(codename=code_permission)
                        
                        if not qs:
                            qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        else:
                            qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        count +=1
                        
                    count = 7
                    
                    for code, name in stock_transfer_type_list:
                        code = code.lower()
                        
                        code_permission = f"can_create_{model_code_name}_type_to_{code}"
                        
                        # Permission Name

                        display_permission = f"Can Create {class_name} Type To {name}"
                        
                        qs = CustomPermission.objects.filter(codename=code_permission)
                        
                        if not qs:
                            qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        else:
                            qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        count +=1
                    
                elif model_class_name in ['ProductStockRequisition']:
                    status_list = REQUISITION_STATUS
                    
                    model_code_name  = ''.join(['_' + c.lower() if c.isupper() else c for c in model_class_name]).lstrip('_')
                    
                    class_name  = re.sub(r'(?<!^)(?=[A-Z])', ' ', model_class_name)
                    
                    code_permission = f"can_approved_{model_code_name}"
                    # Permission Name
                    display_permission = f"Can Approved {class_name}"
                    
                    qs = CustomPermission.objects.filter(codename=code_permission)
                    if not qs:
                        qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                        
                    else:
                        qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                    
                    count = 7
                    
                    for status_code, status_name in status_list:
                        status_code = status_code.lower()
                        
                        code_permission = f"can_update_{model_code_name}_status_to_{status_code}"
                        
                        # Permission Name

                        display_permission = f"Can Update {class_name} Status To {status_name}"
                        
                        qs = CustomPermission.objects.filter(codename=code_permission)
                        
                        if not qs:
                            qs = CustomPermission.objects.create(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        else:
                            qs = qs.update(name = display_permission, codename = code_permission, model_name = model_class_name, serial_no = count, is_active = True)
                            
                        count +=1
                else:
                    model_code_name  = ''.join(['_' + c.lower() if c.isupper() else c for c in model_class_name]).lstrip('_')
                    
                    class_name  = re.sub(r'(?<!^)(?=[A-Z])', ' ', model_class_name)
                    # Code Name

                    list_code_permission = f"can_view_list_{model_code_name}"
                    add_code_permission = f"can_add_{model_code_name}"
                    update_code_permission = f"can_update_{model_code_name}"
                    destroy_code_permission = f"can_destroy_{model_code_name}"
                    retrieve_code_permission = f"can_retrieve_{model_code_name}"
                    menu_show_code_permission = f"can_show_{model_code_name}_menu"
                    download_code_permission = f"can_download_{model_code_name}"
                    upload_code_permission = f"can_upload_{model_code_name}"
                    
                    # Permission Name

                    list_permission = f"Can View {class_name}"
                    add_permission = f"Can Add {class_name}"
                    update_permission = f"Can Update {class_name}"
                    destroy_permission = f"Can Destroy {class_name}"
                    retrieve_permission = f"Can Retrieve {class_name}"
                    menu_show_permission = f"Can Show {class_name} Menu"
                    download_permission = f"Can Download {class_name}"
                    upload_permission = f"Can Upload {class_name}"
                    
                    
                    list_custom_permission_qs = CustomPermission.objects.filter(codename=list_code_permission).last()
                    
                    if not list_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = list_permission, codename = list_code_permission, model_name = model_class_name, serial_no = '1', is_active = True)
                    
                    add_custom_permission_qs = CustomPermission.objects.filter(codename=add_code_permission).last()
                    
                    if not add_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = add_permission, codename = add_code_permission, model_name = model_class_name, serial_no = '2', is_active = True)
                    
                    update_custom_permission_qs = CustomPermission.objects.filter(codename=update_code_permission).last()
                    
                    if not update_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = update_permission, codename = update_code_permission, model_name = model_class_name, serial_no = '3', is_active = True)
                    
                    retrieve_custom_permission_qs = CustomPermission.objects.filter(codename=retrieve_code_permission).last()
                    
                    if not retrieve_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = retrieve_permission, codename = retrieve_code_permission, model_name = model_class_name, serial_no = '4', is_active = True)
                    
                    destroy_custom_permission_qs = CustomPermission.objects.filter(codename=destroy_code_permission).last()
                    
                    if not destroy_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = destroy_permission, codename = destroy_code_permission, model_name = model_class_name, serial_no = '5', is_active = True)
                    
                    menu_show_custom_permission_qs = CustomPermission.objects.filter(codename=menu_show_code_permission).last()
                    
                    if not menu_show_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = menu_show_permission, codename = menu_show_code_permission, model_name = model_class_name, serial_no = '6', is_active = True)
                    
                    download_custom_permission_qs = CustomPermission.objects.filter(codename=download_code_permission).last()
                    
                    if not download_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = download_permission, codename = download_code_permission, model_name = model_class_name, serial_no = '7', is_active = True)
                    
                    upload_custom_permission_qs = CustomPermission.objects.filter(codename=upload_code_permission)
                    
                    if not upload_custom_permission_qs:
                        qs = CustomPermission.objects.create(name = upload_code_permission, codename = upload_code_permission, model_name = model_class_name, serial_no = '8', is_active = True)
                    if not upload_custom_permission_qs:
                        qs = upload_custom_permission_qs.update(name = upload_code_permission, codename = upload_code_permission, model_name = model_class_name, serial_no = '8', is_active = True)
                        
                # Dashboard Permission Start
            
            shop_dashboard_display_permission = 'Can View Shop Dashboard'
            shop_dashboard_code_permission = 'can_view_shop_dashboard'
            
            hrm_dashboard_display_permission = 'Can View HRM Dashboard'
            hrm_dashboard_code_permission = 'can_view_hrm_dashboard'
            
            offline_dashboard_display_permission = 'Can View Offline Dashboard'
            offline_dashboard_code_permission = 'can_view_offline_dashboard'
            
            online_dashboard_display_permission = 'Can View Online Dashboard'
            online_dashboard_code_permission = 'can_view_online_dashboard'
            
            shop_dashboard_display_permission_qs = CustomPermission.objects.filter(codename=shop_dashboard_code_permission)
            
            if not shop_dashboard_display_permission_qs:
                shop_dashboard_display_permission_qs = CustomPermission.objects.create(name = shop_dashboard_display_permission, codename = shop_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            else:
                shop_dashboard_display_permission_qs = shop_dashboard_display_permission_qs.update(name = shop_dashboard_display_permission, codename = shop_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
            
            hrm_dashboard_display_permission_qs = CustomPermission.objects.filter(codename=hrm_dashboard_code_permission)
            
            if not hrm_dashboard_display_permission_qs:
                hrm_dashboard_display_permission_qs = CustomPermission.objects.create(name = hrm_dashboard_display_permission, codename = hrm_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            else:
                hrm_dashboard_display_permission_qs = hrm_dashboard_display_permission_qs.update(name = hrm_dashboard_display_permission, codename = hrm_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
            
            offline_dashboard_display_permission_qs = CustomPermission.objects.filter(codename=offline_dashboard_code_permission)
            
            if not offline_dashboard_display_permission_qs:
                offline_dashboard_display_permission_qs = CustomPermission.objects.create(name = offline_dashboard_display_permission, codename = offline_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            else:
                offline_dashboard_display_permission_qs = offline_dashboard_display_permission_qs.update(name = offline_dashboard_display_permission, codename = offline_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
            
            online_dashboard_display_permission_qs = CustomPermission.objects.filter(codename=online_dashboard_code_permission)
            
            if not online_dashboard_display_permission_qs:
                online_dashboard_display_permission_qs = CustomPermission.objects.create(name = online_dashboard_display_permission, codename = online_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            else:
                online_dashboard_display_permission_qs = online_dashboard_display_permission_qs.update(name = online_dashboard_display_permission, codename = online_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            # Dashboard Permission Start
            
            # Barcode Permission Start
            
            # barcode_display_permission = 'Can View Online Dashboard'
            # barcode_code_permission = 'can_view_online_dashboard'
            
            # shop_dashboard_display_permission_qs = CustomPermission.objects.filter(codename=shop_dashboard_code_permission)
            
            # if not shop_dashboard_display_permission_qs:
            #     shop_dashboard_display_permission_qs = CustomPermission.objects.create(name = shop_dashboard_display_permission, codename = shop_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            # else:
            #     shop_dashboard_display_permission_qs = shop_dashboard_display_permission_qs.update(name = shop_dashboard_display_permission, codename = shop_dashboard_code_permission, model_name = "Dashboard", serial_no = count, is_active = True)
                
            # Barcode Permission Start
            
                        
                        
        return ResponseWrapper(msg='created', status=200)

    
class UserGroupViewSet(CustomViewSet):
    queryset = UserGroup.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = UserGroupSerializer
    
    permission_classes = [permissions.AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = UserGroupFilter
    
    def get_serializer_class(self):
        if self.action in ['user_group_permission_add', 'user_group_permission_remove']:
            self.serializer_class = UserPermissionAddRemoveUpdateSerializer
        elif self.action in ['list']:
            self.serializer_class = UserGroupListSerializer
        elif self.action in ['create', 'update']:
            self.serializer_class = UserGroupCreateUpdateSerializer
        elif self.action in ['permission_add_in_user']:
            self.serializer_class = PermissionAddInUserSerializer
        else:
            self.serializer_class = UserGroupSerializer

        return self.serializer_class

    # ..........***.......... Create ..........***..........
    @log_activity
    def create(self, request, **kwargs):
        is_all_permission = False
        
        is_all_permission = request.data.pop('is_all_permission', None)
        
        custom_permission = request.data.get('custom_permission')
    
        
        name = request.data.get('name')
        
        qs = self.queryset.filter(name = request.data.get('name')) 
        if qs:
            return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
        custom_permission_qs =  CustomPermission.objects.filter(is_active = True)
        
        
        if is_all_permission==True:
            qs = UserGroup.objects.create(name=name)
            qs.custom_permission.set(custom_permission_qs)
            
            serializer = self.serializer_class(qs)
            
        
        else:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            if not serializer.is_valid():
                
                return ResponseWrapper(error_msg=serializer.errors, error_code=400)
            
            if serializer.is_valid():
                # try:
                #     # Create UserGroup without 'is_all_permission' field
                #     qs = serializer.save(created_by=self.request.user)
                # except:
                #     qs = serializer.save()
                # custom_permission_qs = 
                
                qs = UserGroup.objects.create(name=name)
                if custom_permission:
                    qs.custom_permission.set(custom_permission)
                
                user_type_qs = UserType.objects.filter(
                    name = name
                )
                slug = unique_slug_generator(name = name)
                
                if not user_type_qs:
                    user_type_qs = UserType.objects.create(
                        name = name, slug = slug, created_by = request.user
                    )
                else:
                    user_type_qs = user_type_qs.update(
                        name = name, created_by = request.user
                    )

                serializer = self.serializer_class(qs)
            
        activity_log(qs, request,serializer)
                
        return ResponseWrapper(data=serializer.data, msg='created', status=200)
          
    @log_activity
    def update(self, request, **kwargs):
        is_all_permission = False
        
        id = kwargs.get("id")
        
        if request.data.get('is_all_permission'):
            is_all_permission = request.data.pop('is_all_permission')
              
        group_qs = self.queryset.filter(id = id)
        
        if not group_qs:
            return ResponseWrapper(error_msg="User Group is Not Found", error_code=400)
            
        
        if request.data.get('name'):
            user_group_qs = self.queryset.filter(name = request.data.get('name'))
        
            if user_group_qs and not user_group_qs.last().id == id:
                return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
        
        custom_permission_qs =  CustomPermission.objects.filter(is_active = True)
        
        
        if request.data.get('name'):
            name = request.data.get('name')
        else:
            name = group_qs.last().name
        
        if is_all_permission:
            qs = group_qs.update(name=name)
            group_qs.last().custom_permission.set(custom_permission_qs)
            
            serializer = self.serializer_class(group_qs.last())

        else:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
        
            if not serializer.is_valid():
                return ResponseWrapper(error_msg=serializer.errors, error_code=400)
            
            if serializer.is_valid():
                qs = serializer.update(instance=group_qs.last(), validated_data=serializer.validated_data)
                    
                # qs = UserGroup.objects.filter(id = qs.id).last()
                    
                serializer = self.serializer_class(qs)
                
                user_list = UserAccount.objects.filter(groups__id = id)
                
                # if user_list:
                #     for user in user_list:
                #         custom_permission_list = qs.custom_permission.values_list('id', flat=True)
                #         for permission_id in custom_permission_list:
                #             user.custom_permission.add(permission_id)
                #         print(f'User = {user.email}')
                
        activity_log(qs, request,serializer)
                
        return ResponseWrapper(data=serializer.data, msg='created', status=200)

    @log_activity
    def user_group_permission_add(self, request,group_id, **kwargs):
        qs = self.queryset.filter(id=group_id).last()
        
        if not qs:
            return ResponseWrapper(
                error_msg='User Group is Not Found', error_code=404
            )
        custom_permission_list = request.data.get('custom_permission')
        for custom_permission_id in custom_permission_list:
            custom_permission = CustomPermission.objects.filter(id=custom_permission_id).first()
            if custom_permission:
                qs.custom_permission.add(custom_permission)
                
                # Update user accounts related to this permission
                # user_qs = UserAccount.objects.filter(groups__id=group_id)
                # if user_qs:
                #     for user in user_qs:
                #         user.custom_permission.add(custom_permission)
        
        serializer = self.serializer_class(instance=qs)
        return ResponseWrapper(data=serializer.data, msg='Successfully Update')
    
    @log_activity
    def user_group_permission_remove(self, request,group_id, **kwargs):
        qs = self.queryset.filter(id=group_id).last()
        
        if not qs:
            return ResponseWrapper(
                error_msg='User Group is Not Found', error_code=404
            )
        custom_permission_list = request.data.get('custom_permission')
        for custom_permission_id in custom_permission_list:
            custom_permission = CustomPermission.objects.filter(id=custom_permission_id).first()
            if custom_permission:
                qs.custom_permission.remove(custom_permission)
                
                # Update user accounts related to this permission
                user_qs = UserAccount.objects.filter(groups__id=group_id)
                if user_qs:
                    for user in user_qs:
                        user.custom_permission.remove(custom_permission)
        
        serializer = self.serializer_class(instance=qs)
        return ResponseWrapper(data=serializer.data, msg='Successfully Update')

    @log_activity
    def permission_add_in_user(self, request, group_id, *args, **kwargs):
        qs = self.queryset.filter(id=group_id).last()
        
        if not qs:
            return ResponseWrapper(
                error_msg='User Group is Not Found', error_code=404
            )
        
        permission_list = qs.custom_permission.all()
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, many=True) 
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        data_list = request.data
        for item in data_list:
            employee_slug = item.get("employee_slug")
            employee_qs = EmployeeInformation.objects.filter(
                slug = employee_slug
            ).last()
            
            if not employee_qs:
                return ResponseWrapper(error_msg=f'{employee_slug} is not Found', error_code=404)
            
            employee_user_qs = UserAccount.objects.filter(id = employee_qs.user.id).last()
            
            for permission in permission_list:
                employee_user_qs.custom_permission.add(permission)
            employee_user_qs.groups.add(qs)
        
        return ResponseWrapper(msg="Success", status=200)

    @log_activity
    def user_permission_list(self, request, permission_type, *args, **kwargs):
        qs  = CustomPermission.objects.filter(user_groups__name__icontains = permission_type, is_active = True).order_by('id')
        
        if permission_type == 'super_user':
            qs  = CustomPermission.objects.filter(is_active = True).order_by('id')
            
        elif permission_type == 'accounts':
            qs  = CustomPermission.objects.filter(user_groups__name ="Accounts", is_active = True).order_by('id')
            
        elif permission_type == 'warehouse_manager':
            qs  = CustomPermission.objects.filter(user_groups__name__icontains = 'warehouse').order_by('id') 
            
        serializer = CustomPermissionSerializer(qs, many=True)

        # page_qs = self.paginate_queryset(qs)
        # serializer = CustomPermissionSerializer(instance=page_qs, many=True)

        # paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status=200)


class UserTypeViewSet(CustomViewSet):
    queryset = UserType.objects.all()
    lookup_field = 'pk'
    serializer_class = UserTypeSerializer
    permission_classes = [IsAuthenticated]
    
    
class AdminUserViewSet(CustomViewSet):
    queryset = UserInformation.objects.all()
    lookup_field = 'pk'
    serializer_class = UserInformationSerializer
    permission_classes = [IsAuthenticated]
    
    permission_classes = [permissions.AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = UserInformationFilter
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = UserRegistrationSerializer
        elif self.action in ['update']:
            self.serializer_class = UserUpdateSerializer
        elif self.action in ['employee_user_information_update']:
            self.serializer_class = UserUpdateSerializer
        elif self.action in ['list']:
            self.serializer_class = UserInformationListSerializer
        else:
            self.serializer_class = UserInformationSerializer

        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["create"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @log_activity
    def customer_overview_list(self, request, *args, **kwargs):
        today = settings.TODAY
        
        user_information_qs = UserInformation.objects.filter(
            user_type__name="Customer"
        )
        
        total_customer = user_information_qs.count()
        total_customer_ratio = total_customer * 100 / total_customer if total_customer else 0
        
        this_month = today.month
        last_month = (today - relativedelta(months=1)).month
        
        this_month_joining_total_customer = user_information_qs.filter(created_at__month=this_month).count()
        this_month_joining_total_customer_ratio = this_month_joining_total_customer * 100 / total_customer if total_customer else 0
        
        last_month_joining_total_customer = user_information_qs.filter(created_at__month=last_month).count()
        last_month_joining_total_customer_ratio = last_month_joining_total_customer * 100 / total_customer if total_customer else 0
        
        ecommerce_total_customer = user_information_qs.filter(orders__order_type = "ECOMMERCE_SELL").count()
        ecommerce_total_customer_ratio = ecommerce_total_customer * 100 / total_customer if total_customer else 0
        
        
        context = [
            {
                'msg': "Total Active Customer",
                'quantity': total_customer,
                'ratio': f"{total_customer_ratio}%",
            },
            {
                'msg': "This Month Total Joining Customer",
                'quantity': this_month_joining_total_customer,
                'ratio': f"{round(this_month_joining_total_customer_ratio, 2)}%",
            },
            {
                'msg': "Last Month Total Joining Customer",
                'quantity': last_month_joining_total_customer,
                'ratio': f"{round(last_month_joining_total_customer_ratio, 2)}%",
            },
            {
                'msg': "This E-Commerce Customer",
                'quantity': ecommerce_total_customer,
                'ratio': f"{round(ecommerce_total_customer_ratio, 2)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    # ..........***.......... Create ..........***..........
    @log_activity
    def create(self, request, *args, **kwargs):
        password = request.data.pop("password")
        user_type = request.data.pop("user_type")
        email = request.data.get("email")
        phone_number = request.data.pop("phone")
        
        groups = request.data.get("groups")
        
        groups_last = None
        
        if groups:
            groups_last = groups[0]
            groups = request.data.pop("groups")
        
        email_exist = UserAccount.objects.filter(email=email).exists()

        if email_exist:
            return ResponseWrapper(
                error_msg="Email is Already Used", status=400
            )
            
        if phone_number.startswith("+880"):
            phone = phone_number[3:]  # Remove the '+880' prefix
        elif not phone_number.startswith("01"):
            phone = "01" + phone_number  # Add '01' prefix
        else:
            phone = phone_number
        
        phone_exist = UserAccount.objects.filter(phone=phone).exists()

        if phone_exist:
            return ResponseWrapper(
                error_msg="Phone Number is Already Used", status=400
            )
            
        if user_type:
            user_type_qs = UserType.objects.filter(slug=user_type).last()
            
            if not user_type_qs:
                return ResponseWrapper(
                    error_msg="User Type is Not Found", status=404
                )
                
        else:                
            user_type_qs = UserType.objects.filter(name__iexact='regular').last()
        
        password = make_password(password=password)
        user = UserAccount.objects.create(
            password=password,
            phone=phone,
            **request.data
        )
        if groups_last:
            user.groups.add(groups_last)
        
        refresh_token = RefreshToken.for_user(user)
        token = str(refresh_token.access_token)
                
        name = f"{user.first_name} {user.last_name}"
        
        user_information_qs = UserInformation.objects.create(
            name=name, user_id=user.id, created_by=self.request.user
        )
        if user_type_qs:
            user_information_qs.user_type_id = user_type_qs.id
            user_information_qs.save()
        
        # user_information_qs = UserInformation.objects.filter(
        #     user__email = email
        # ).last()
        
        serializer = UserInformationSerializer(instance=user_information_qs)

        context = {
            'user_info': serializer.data,
            # 'token': token,
        }
        return ResponseWrapper(data=context, status=200)
    
    @log_activity
    def update(self, request, id, *args, **kwargs):
        user_type = request.data.pop("user_type", None)
        user_information_qs = self.queryset.filter(id=id).last()

        if not user_information_qs:
            return ResponseWrapper(
                error_msg="User Information is Not Found", status=404
            )

        user_type_qs = None
        if user_type:
            user_type_qs = UserType.objects.filter(id=user_type).last()

            if not user_type_qs:
                return ResponseWrapper(
                    error_msg="User Type is Not Found", status=404
                )
        else:
            user_type_qs = UserType.objects.filter(name__iexact='Customer').last()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=user_information_qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            user_qs = UserAccount.objects.filter(id=user_information_qs.user.id).last()
            if not user_qs:
                return ResponseWrapper(
                    error_msg="User is Not Found", status=404
                )

            first_name = request.data.get("first_name", user_qs.first_name)
            last_name = request.data.get("last_name", user_qs.last_name)
            is_active = request.data.get("is_active", user_qs.is_active)

            user_qs.first_name = first_name
            user_qs.last_name = last_name
            user_qs.is_active = is_active
            user_qs.save()
            
            name = f"{first_name} {last_name}"
            user_information_qs.name = name

            if user_type_qs:
                user_information_qs.user_type_id = user_type_qs.id

            user_information_qs.save()

            serializer = UserInformationSerializer(instance=user_information_qs)
            
            return ResponseWrapper(data=serializer.data, status=200, msg="User Information Successfully Updated")
        
        return ResponseWrapper(error_msg=serializer.errors, status=400)
    
    @log_activity
    def employee_user_information_update(self, request, employee_slug, *args, **kwargs):
        employee_qs = EmployeeInformation.objects.filter(slug = employee_slug).last()
        if not employee_qs:
            return ResponseWrapper(
                error_msg="Employee Information is Not Found", status=404
            )
            
        user_type = request.data.pop("user_type", None)
        
        user_information_qs = UserAccount.objects.filter(id=employee_qs.user.id).last()

        if not user_information_qs:
            return ResponseWrapper(
                error_msg="User Information is Not Found", status=404
            )

        user_type_qs = None
        if user_type:
            user_type_qs = UserType.objects.filter(slug=user_type).last()

            if not user_type_qs:
                return ResponseWrapper(
                    error_msg="User Type is Not Found", status=404
                )
        else:
            user_type_qs = UserType.objects.filter(name__iexact='Customer').last()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=user_information_qs, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            
            user_qs = UserAccount.objects.filter(id=employee_qs.user.id).last()
            
            if not user_qs:
                return ResponseWrapper(
                    error_msg="User is Not Found", status=404
                )

            first_name = request.data.get("first_name", user_qs.first_name)
            last_name = request.data.get("last_name", user_qs.last_name)
            is_active = request.data.get("is_active", user_qs.is_active)

            user_qs.first_name = first_name
            user_qs.last_name = last_name
            user_qs.is_active = is_active
            user_qs.save()
            
            name = f"{first_name} {last_name}"
            user_information_qs.name = name

            if user_type_qs:
                user_information_qs.user_type_id = user_type_qs.id

            user_information_qs.save()
            
            
            qs = UserInformation.objects.filter(
                user = employee_qs.user
            ).last()


            serializer = UserInformationSerializer(instance=qs)
            
            return ResponseWrapper(data=serializer.data, status=200, msg="User Information Successfully Updated")
        
        return ResponseWrapper(error_msg=serializer.errors, status=400)

class UserDownloadViewSet(CustomViewSet):
    queryset = UserInformation.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = UserInformationDownloadSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = UserInformationFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [
                    CheckCustomPermission("can_view_list_user_information")
                ]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @staticmethod
    async def generate_excel(serializer_data):
        df = pd.DataFrame(serializer_data)
        stream = io.BytesIO()
        df.to_excel(stream, index=False)
        stream.seek(0)
        return stream.getvalue()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @log_activity
    def list(self, request, *args, **kwargs):
        from openpyxl import Workbook
        from django.db import connection
        # queryset = self.get_queryset()
        
        # # Handle query parameters for filtering and ordering
        # filter_backend = DjangoFilterBackend()
        # queryset = filter_backend.filter_queryset(request, queryset, self)
        
        # ordering_backend = filters.OrderingFilter()
        # queryset = ordering_backend.filter_queryset(request, queryset, self)
        try:
            search = request.GET.get('search')
            joining_start_date = request.GET.get('joining_start_date')
            joining_end_date = request.GET.get('joining_end_date')
            order_start_date = request.GET.get('order_start_date')
            order_end_date = request.GET.get('order_end_date')
            division = request.GET.get('division')
            district = request.GET.get('district')
            area = request.GET.get('area')

            # Start building the base query
            base_query = """
                SELECT
                    ROW_NUMBER() OVER (ORDER BY ua.id) AS SI,
                    ua.first_name AS "First Name",
                    ua.last_name AS "Last Name",
                    ua.email AS "Email",
                    ua.phone AS "Contact Number",
                    a.name AS "Area",
                    cal.division_name AS "Division",
                    cal.district_name AS "District",
                    cal.address AS "Address",
                    ua.is_active AS "Active Status",
                    ut.name AS "Customer Type",
                    o.order_type AS "Order Type",
                    ua.date_joined AS "Joining Date",
                    COUNT(o.id) AS "Total Order",
                    SUM(CASE WHEN o.status = 'DISPATCHED' THEN 1 ELSE 0 END) AS "Total Dispatched Order",
                    SUM(CASE WHEN o.status = 'DELIVERED' THEN 1 ELSE 0 END) AS "Total Delivered Order",
                    SUM(CASE WHEN o.status = 'CANCELLED' THEN 1 ELSE 0 END) AS "Total Cancel Order",
                    SUM(CASE WHEN o.status = 'RETURNED' THEN 1 ELSE 0 END) AS "Total Return Order",
                    SUM(CASE WHEN o.status = 'PROCESSING' THEN 1 ELSE 0 END) AS "Total Processing Order",
                    SUM(o.total_gsheba_amount) AS "Total G-Sheba Amount"
                FROM
                    user_useraccount ua
                LEFT JOIN
                    user_userinformation ui ON ua.id = ui.user_id
                LEFT JOIN
                    order_order o ON ui.id = o.customer_id
                LEFT JOIN
                    user_usertype ut ON ui.user_type_id = ut.id
                LEFT JOIN
                    order_customeraddressinfolog cal ON o.id = cal.order_id
                LEFT JOIN
                    location_area a ON o.area_id = a.id
            """

            # Define the where conditions
            where_conditions = [
                "ua.is_superuser IS False",
                "ua.is_staff IS False",
                "ua.first_name NOT ILIKE '%test%'",
                "ua.last_name NOT ILIKE '%test%'",
                "ua.email NOT ILIKE '%test%'",
                "ua.phone NOT ILIKE '%test%'",
                "ua.phone IS NOT NULL"
            ]

            if search:
                search_condition = (
                    f"ua.first_name ILIKE '%{search}%' OR "
                    f"ua.last_name ILIKE '%{search}%' OR "
                    f"ua.email ILIKE '%{search}%' OR "
                    f"ua.phone ILIKE '%{search}%'"
                )
                where_conditions.append(f"({search_condition})")

            if joining_start_date and joining_end_date:
                where_conditions.append(f"ua.date_joined BETWEEN '{joining_start_date}' AND '{joining_end_date}'")

            if order_start_date and order_end_date:
                where_conditions.append(f"o.order_date BETWEEN '{order_start_date}' AND '{order_end_date}'")

            if division:
                where_conditions.append(f"cal.division_name = '{division}'")

            if district:
                where_conditions.append(f"cal.district_name = '{district}'")

            if area:
                where_conditions.append(f"a.name = '{area}'")

            # Append the conditions to the base query
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)

            # Group by non-aggregated columns
            base_query += """
                GROUP BY
                    ua.id, ua.first_name, ua.last_name, ua.email, ua.phone, cal.division_name, cal.district_name, cal.address, 
                    ua.is_active, ut.name, o.order_type, ua.date_joined, a.name
                ORDER BY
                    ua.id;
            """

            # Execute the query and fetch data
            with connection.cursor() as cursor:
                cursor.execute(base_query)
                rows = cursor.fetchall()

            # Initialize workbook and worksheet
            wb = Workbook()
            ws = wb.active

            # Define headers
            headers = [
                'SI',
                'First Name',
                'Last Name',
                'Username',  # This column will be left empty as it is not fetched from the query
                'Email',
                'Contact Number',
                'Area',
                'Division',
                'District',
                'Address',
                'Active Status',
                'Customer Type',
                'Order Type',
                'Joining Date',
                'Total Order',
                'Total Dispatched Order',
                'Total Delivered Order',
                'Total Cancel Order',
                'Total Return Order',
                'Total Processing Order',
                'Total G-Sheba Amount'
            ]
            ws.append(headers)

            # Loop through fetched rows and add data to worksheet
            for row in rows:
                row = list(row)
                # Remove timezone information from datetime objects
                for i, value in enumerate(row):
                    if isinstance(value, datetime) and value.tzinfo is not None:
                        row[i] = value.replace(tzinfo=None)
                # Insert an empty value for the "Username" column
                row.insert(3, '')  
                ws.append(row)

            # Save the workbook
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="Customer-{datetime.now().strftime("%Y-%m-%d")}.xlsx"'

            try:
                wb.save(response)
            except Exception as e:
                print(f"Error saving workbook: {e}")
                return HttpResponse(status=500)

            return response

        except Exception as e:
            print(f"Error in view: {e}")
            return HttpResponse(status=500)