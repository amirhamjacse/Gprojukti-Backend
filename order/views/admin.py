import random
from django.conf import settings
from courier_management.models import Courier, CourierService
from discount.models import PromoCode
from gporjukti_backend_v2.settings import BASE_URL, TODAY
from order.models import *
from order.serializers import *
from human_resource_management.models.employee import EmployeeInformation
from product_management.models.product import ProductStock, Product
from product_management.utils import barcode_status_log
from user.models import UserType
from utils.actions import activity_log
from utils.calculate import generate_service_order_status_log, service_order_create_or_update, generate_order_status_log, offer_check, order_item_create, order_payment_log
from utils.custom_pagination import CustomPageNumberPagination
from utils.custom_veinlet import CustomViewSet
from utils.decorators import log_activity
from utils.fcm import send_fcm_push_notification_appointment
from utils.generates import generate_invoice_no, generate_service_invoice_no, unique_slug_generator
from utils.permissions import CheckCustomPermission
from utils.response_wrapper import ResponseWrapper
from utils.send_sms import send_email

from utils.upload_image import image_upload
from django.utils import timezone
from order.filters import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from utils.base import get_user_store_list, render_to_pdf
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.db import transaction
from django.shortcuts import get_object_or_404
from io import BytesIO
import csv
import time

from django.db import connection
from openpyxl import Workbook

from concurrent.futures import ThreadPoolExecutor, as_completed


import os
import zipfile
import asyncio

import io
import openpyxl

from django.core.paginator import Paginator
import pandas as pd

from django.http import StreamingHttpResponse
from rest_framework.response import Response
from tablib import Dataset
from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from channels.layers import get_channel_layer
from django.template.loader import render_to_string

import logging

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def order_status_overview(queryset, status, msg):
    quantity = 0
    ratio = 0
    
    qs = queryset.filter(status=status)
    quantity = qs.count()
    ratio = round((quantity / queryset.count()) * 100, 2)
    
    context = {
        'msg': msg,
        'quantity': quantity,
        'ratio': f"{str(ratio)}%",
    }
    
    return context

class DeliveryMethodViewSet(CustomViewSet):
    queryset = DeliveryMethod.objects.all()
    lookup_field = 'pk'
    serializer_class = DeliveryMethodListSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    # filterset_class = OrderFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        elif self.action in ["create",]:
            permission_classes = [IsAuthenticated]
            
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 
    
class OrderViewSet(CustomViewSet):
    queryset = Order.objects.all().exclude(total_payable_amount = 0.0).order_by('-order_date')
    lookup_field = 'pk'
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = OrderFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["multiple_order_invoice_print","pos_invoice_print" "multiple_order_label_print", "order_invoice_print", "order_item_status_log"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = OrderCreateSerializer
        elif self.action in ['list']:
            self.serializer_class = OrderListSerializer
        elif self.action in ['order_details']:
            self.serializer_class = OrderDetailsSerializer
        elif self.action in ['order_customer_info_address_update']:
            self.serializer_class = CustomerInformationAddressUpdateSerializer
        elif self.action in ['order_status_update']:
            self.serializer_class = OrderStatusUpdateSerializer
        elif self.action in ['order_return_status_update']:
            self.serializer_class = OrderReturnStatusUpdateSerializer
        elif self.action in ['gsheba_return_item_add']:
            self.serializer_class = OrderItemReturnUpdateSerializer
        elif self.action in ['order_return_status_approved_rejected']:
            self.serializer_class = OrderReturnStatusApprovedRejectedSerializer
        elif self.action in ['order_item_update']:
            self.serializer_class = OrderItemCreateUpdateSerializer
        elif self.action in ['order_payment_log_update', 'order_refunded_payment_update']:
            self.serializer_class = OrderPaymentLogCreateSerializer
        elif self.action in ['order_item_status_log']:
            self.serializer_class = OrderItemStatusLogListSerializer
        elif self.action in ['multiple_order_invoice_print', 'multiple_order_label_print']:
            self.serializer_class = MultipleInvoiceListSerializer
        elif self.action in ['apply_promo_code']:
            self.serializer_class = ApplyPromoCodeSerializer
        elif self.action in ['courier_service_add_in_order']:
            self.serializer_class = CourierServiceAddInOrderSerializer
        elif self.action in ['order_remarks']:
            self.serializer_class = OrderRemarkSerializer
        else:
            self.serializer_class = OrderListSerializer

        return self.serializer_class
    
    # def get_permissions(self):
    #     if self.action in ["multiple_order_invoice_print", "multiple_order_label_print", "order_invoice_print", "order_item_status_log"]:
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAuthenticated]
            
    #     return [permission() for permission in permission_classes]

    # ..........***.......... Get All Data ..........***..........
    
    
    
    def order_payment_details(self, request,invoice_no,  *args, **kwargs):
        order_payment_qs = OrderPaymentLog.objects.filter(
            order__invoice_no = invoice_no
        ).last()
        
        if not order_payment_qs:
            return ResponseWrapper(error_code=404, error_msg=f"Order Payment Details iS Not Found")
        
        order_qs = Order.objects.filter(invoice_no=invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_code=404, error_msg=f"Order is not Found")
        
        
        transaction_no = order_payment_qs.transaction_no
        
        params = {
                    'tran_id': transaction_no,
                    'store_id': settings.SSL_STORE_ID,
                    'store_passwd': settings.SSL_STORE_PASSWORD,
                }
        
            
        response = requests.get('https://securepay.sslcommerz.com/validator/api/merchantTransIDvalidationAPI.php', params=params)
        
        if response.json()['element'][0]['status'] == 'VALID' or response.json()['element'][0]['status'] == 'VALIDATED':
            
            print(f"DEatils = {response.json()}")
            
            order_qs.payment_status = "PAID"
            order_qs.save()
            
            payment_type_name = response.json()['element'][0]['card_issuer']
            
            payment_type_qs  =  PaymentType.objects.filter(name__icontains = payment_type_name).last()
            
            if payment_type_qs:
                order_payment_qs.order_payment = payment_type_qs
                order_payment_qs.save()
        
        return ResponseWrapper(msg='Payment Success', status=200)
    
    @log_activity
    def list(self, request, *args, **kwargs):
        
        user_type_qs = UserInformation.objects.filter(user = request.user).last()
        qs = self.filter_queryset(self.get_queryset()) 
        
        if request.user.is_superuser:
            qs = qs.filter()
                
        elif user_type_qs:
            shop_qs = get_user_store_list(request.user)
            shop_slug_list = shop_qs.values_list('slug', flat=True) 
            
            if user_type_qs.user_type.name in ["Shop", "Shop User", "RIC"]:
                qs = qs.filter(
                    Q(shop__slug__in = shop_slug_list)
                    | Q(pickup_shop__slug__in = shop_slug_list)
                    | Q(return_shop__slug__in = shop_slug_list)
                    | Q(created_by = request.user)
                )
        
        else:
            qs = qs.filter()
            
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)


    # # ..........***.......... Create ..........***..........
    @log_activity
    def order_overview_list(self, request,order_type, *args, **kwargs):
        order_qs = Order.objects.filter(order_type = order_type)
        
        order_list = []
        all_order_status_list = ORDER_STATUS
        
        for status_tuple in all_order_status_list:
            full_status, status_display = status_tuple 
            
            order_details = order_status_overview(
                queryset=order_qs, 
                status=full_status, 
                msg=f'Total {status_display}')
            order_list.append(order_details)
        
        # context = [
        #     {
        #         'msg': "Order Received",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Product Availability Check",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Order Confirmed",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Product Purchased",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Preliminary QC",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Detailed QC",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Packaged",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     },
        #     {
        #         'msg': "Ready for Pickup",
        #         'quantity': random.randint(333, 7342),
        #         'ratio': f"{random.randint(21, 99)}%",
        #     }
        # ]
        return ResponseWrapper(data= order_list, msg="Success", status=200)
    
    @log_activity
    def return_overview_list(self, request, *args, **kwargs):
        context = [
            {
                'msg': "Total Return Order",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total G-Sheba Return Order",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Replacement Order",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Refunded Order",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    @log_activity
    def return_order_list(self, request, *args, **kwargs):
        qs = Order.objects.filter(status__in = ['RETURNED', 'REFUNDED', 'GSHEBA_RETURNED'])
        qs = self.filter_queryset(qs)
        
        page_qs = self.paginate_queryset(qs)
        serializer = OrderListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

            
    @log_activity
    def create(self, request, *args, **kwargs):
        # from django.template.loader import render_to_string
        # logger.info("Order creation started")
        
        order_date = request.data.get('order_date')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        area_slug = request.data.get('area_slug')
        address = request.data.get('address')
        address_type = request.data.get('address_type')
        delivery_method_slug = request.data.get('delivery_method_slug')
        order_type = request.data.get('order_type')
        payment_type = request.data.get('payment_type')
        promo_code = request.data.get('promo_code')
        employee_id = request.data.get('employee_id')
        total_advance_amount = request.data.get('total_advance_amount')
        shop = request.data.get('shop')
        pickup_shop = request.data.get('pickup_shop')
        is_for_employee = request.data.get('is_for_employee')
        
        remarks = '-'
        
        try:
            remarks = request.data.get('remarks')
        except:
            remarks = '-'
        
        order_item_list = request.data.get('order_item_list')
        order_payment_list = request.data.get('order_payment_list')
        
        shop_qs = None
        pickup_shop_qs = None
        delivery_method_qs = None
        payment_qs = None
        
        approved_status = "APPROVED"
        
        delivery_method_qs = DeliveryMethod.objects.filter(delivery_type = "STORE_SELL").last()
            
        if not order_type in ['POINT_OF_SELL']:
            delivery_method_qs = DeliveryMethod.objects.filter(delivery_type = delivery_method_slug).last()
            
            if not delivery_method_qs:
                return ResponseWrapper(error_msg='Delivery Method is Not Found', status=404)
            
        payment_type = "PAY_AT_STORE"
        
        # if not payment_type:
            # return ResponseWrapper(error_msg='Payment Type is Mandatory', status=404)
        
        if not order_type in ['POINT_OF_SELL'] and not shop:
            if delivery_method_qs.delivery_type in ["SHOP_PICKUP", "STORE_SELL"] and not pickup_shop:
                
                logger.error("Pickup Shop ID is mandatory for the selected delivery method")
                return ResponseWrapper(error_msg=f'For Store Pickup,  Shop Name is Mandatory', status=400)
        
        user_qs = UserAccount.objects.filter(Q(email=email) | Q(phone=phone)).last()

        if not user_qs:
            user_qs = UserAccount.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone)
        
        name = f"{first_name} {last_name}"
        
        user_information_qs = UserInformation.objects.filter(user__id=user_qs.id).last()
        
        if not user_information_qs:
            user_info_slug = unique_slug_generator(name=name) if name else None
            user_type = 'Corporate' if order_type == 'CORPORATE_SELL' else 'Customer'
            user_type_qs = UserType.objects.filter(name=user_type).last()
            
            if not user_type_qs:
                user_type_qs = UserType.objects.create(name=user_type)
            
            user_information_qs = UserInformation.objects.create(
                name=name, slug=user_info_slug, user_type=user_type_qs, created_by=request.user, user=user_qs
            )
            
        if is_for_employee == True:
            user_qs = EmployeeInformation.objects.filter(
                user__email = user_information_qs.user.email
            ).last()
            
            if not user_qs:
                return ResponseWrapper(error_msg='For Employee Order, Employee Information Is Not Found', error_code=404, status=400)
            
            approved_status = "INITIALIZED"
        
        if not area_slug and not order_type in ['POINT_OF_SELL']:
            return ResponseWrapper(error_msg='Area is Mandatory', error_code=404, status=400)
        
        # if order_type in ['POINT_OF_SELL']:
            
        #     area_slug = shop_qs
            
        area_qs = Area.objects.filter(slug=area_slug).last()

        if not area_qs:
            return ResponseWrapper(error_msg=f'Area is Not Found', status=404)
        
        area_name = area_qs.name if area_qs else '-'
        
        district_name = area_qs.district.name if area_qs and area_qs.district else '-'
        division_name = area_qs.district.division.name if area_qs and area_qs.district and area_qs.district.division else '-'
        country_name = area_qs.district.division.country.name if area_qs and area_qs.district and area_qs.district.division and area_qs.district.division.country else 'Bangladesh'
        
        
        last_order_qs = Order.objects.all().order_by('-created_at').last()
        
        last_invoice_no = last_order_qs.invoice_no if last_order_qs else 'ONL000000001'
        invoice_no = generate_invoice_no(last_invoice_no)
        today = timezone.now()
        order_create_user = request.user
        employee_qs= None

        if employee_id:
            employee_qs = EmployeeInformation.objects.filter(employee_id=employee_id).last()
            
            if not employee_qs:
                logger.error("Employee information not found")
                return ResponseWrapper(error_msg=f'Employee Information {employee_id}, is Not Found', status=404)
            
            order_create_user = employee_qs.user
        if order_type == 'PRE_ORDER' and not order_date:
            logger.error("Order date is mandatory for pre-orders")
            return ResponseWrapper(error_msg='Order Date is Mandatory', status=400)
        
        status = 'ORDER_RECEIVED' if order_type != 'POINT_OF_SELL' else 'DELIVERED'
        
        if shop:
            shop_qs = OfficeLocation.objects.filter(slug=shop, office_type="STORE").last()
            
            if not shop_qs:
                return ResponseWrapper(error_msg=f"{shop}, is Not Found", error_code=404)
            
        if shop_qs and order_type in ["ECOMMERCE_SELL", "RETAIL_ECOMMERCE_SELL"]:
            pickup_shop_qs = shop_qs
        
        if pickup_shop:
            pickup_shop_qs = OfficeLocation.objects.filter(slug=pickup_shop, office_type="STORE").last()
            if not pickup_shop_qs:
                logger.error("Pickup shop not found")
                return ResponseWrapper(error_msg=f"{shop}, is Not Found", error_code=404)
        
        if not shop and order_type in ['POINT_OF_SELL', "ON_THE_GO", "CORPORATE_SELL", "B2B_SELL", "RETAIL_ECOMMERCE_SELL"]:
            employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            
            if employee_qs:
                if not employee_qs.work_station:
                    return ResponseWrapper(error_msg=f"Shop Information is Not Found", error_code=404)
                
                shop_qs = employee_qs.work_station
        
        
        if order_type in ['POINT_OF_SELL', "RETAIL_ECOMMERCE_SELL"]:
            shop_qs = shop_qs
            
        order_qs = Order.objects.create(
            invoice_no=invoice_no,
            order_type=order_type,
            approved_status=approved_status,
            status=status,
            customer=user_information_qs,
            delivery_method=delivery_method_qs,
            payment_status='UNPAID',
            payment_type=payment_type,
            area=area_qs,
            district_name=district_name,
            division_name=division_name,
            country_name=country_name,
            address=address,
            promo_code=promo_code,
            is_for_employee=is_for_employee,
            pickup_shop=pickup_shop_qs,
            created_by=order_create_user,
            remarks=remarks,
        )
        
        print(f"New Create Order Invoice No is  = {invoice_no}")
        
        try:
            created_date_str = order_qs.created_at.strftime('%d %B, %Y at %I:%M %p')
        
            user_notification_qs = UserNotification.objects.create(
                    title = f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()}",
                    description=f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()} By {request.user.email} at {created_date_str}",
                    created_by = request.user, 
                    user_information= request.user
                ) 
            
            print(f"User Notification Created for = {request.user.email} Successfully and which is {user_notification_qs.title}")
            
            
            channel_layer = get_channel_layer()
            
            group_name = f'admin-panel-{request.user.id}'
            
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification',
                    'data': f"An {order_qs.get_order_type_display()} Has Been Received"
                    # 'order': serializer.data
                }
            )
            # logger.info(f'Notification sent for user {order_create_user.id} with order data: {serializer.data}')
            
        except Exception as e:
            logger.error(f'Error sending notification: {e}')
            
        print(f"Shop Name = {shop_qs}")
        
        if not order_date:
            order_date = order_qs.created_at
            order_qs.save()
        
        if order_qs and order_date:
            order_qs.order_date = order_date
            order_qs.save()
        
        if order_qs.order_type == 'RETAIL_ECOMMERCE_SELL':
            order_qs.shop = shop_qs
            order_qs.save()
        
        elif shop_qs and not order_type in ["ECOMMERCE_SELL"]:
            order_qs.shop = shop_qs
            order_qs.save()
            
        elif shop_qs and not order_type in ["ECOMMERCE_SELL"]:
            order_qs.shop = shop_qs
            order_qs.save()
        
        elif pickup_shop_qs:
            order_qs.pickup_shop = pickup_shop_qs
            order_qs.save()
        
        # order_qs.save()
        
        user_address_slug = unique_slug_generator(name=name) if name else None
        
        CustomerAddressInfoLog.objects.create(
            address_type=address_type, slug=user_address_slug,
            name=name, phone=phone, email=email,
            address=address, area_name=area_name, district_name=district_name,
            division_name=division_name, country_name=country_name,
            created_by=order_create_user, order=order_qs
        )
        
        for order_item in order_item_list:
            product_slug = order_item.get('product_slug')
            quantity = order_item.get('quantity')
            selling_price = order_item.get('selling_price') or 0.0
            gsheba_amount = order_item.get('gsheba_amount')
            barcode_number = order_item.get('barcode_number')
            
            if order_type in ["POINT_OF_SELL", "CORPORATE_SELL", "B2B_SELL"] and not barcode_number:
                
                order_type_display = order_qs.get_order_type_display()
                order_qs.delete()
                
                return ResponseWrapper(error_msg=f"For {order_type_display}, Barcode is Mandatory", error_code=400, status=400)
            
            if barcode_number:
                product_stock_qs = ProductStock.objects.filter(barcode = barcode_number, status = "ACTIVE").last()
                
                if not product_stock_qs:
                    order_qs.delete()
                    return ResponseWrapper(error_msg=f"'{barcode_number}' is Not Found", error_code=400, status=400)
                
                if product_stock_qs.product_price_info:
                    msp = product_stock_qs.product_price_info.msp
                    mrp = product_stock_qs.product_price_info.mrp
                    
                    if selling_price > mrp:  
                        order_qs.delete()
                        return ResponseWrapper(error_msg=f"Product Price Must Be Less Then MRP", error_code=400, status=400)
                    
                    elif selling_price < msp:  
                        order_qs.delete()
                        return ResponseWrapper(error_msg=f"Product Price Must Be greater Then MSP", error_code=400, status=400)
                
            created_by = order_item.get('created_by')
            
            order_item_created_by = request.user
            
            new_time = order_qs.created_at + timedelta(hours=6)
            
            created_at_str = new_time.strftime("%d %B, %Y %I:%M %p")
                
            status_change_reason = f'Order Item Created By - {request.user.email} at {created_at_str}'
            
            if created_by:
                order_item_created_by_qs = EmployeeInformation.objects.filter(employee_id = created_by).last()
            
                if not order_item_created_by_qs:
                    order_qs.delete()
                    return ResponseWrapper(error_code=404, error_msg=f'{created_by} Employee Id is Not Found', status=404)
                
                order_item_created_by = order_item_created_by_qs.user
            
                created_at_str = new_time.strftime("%d %B, %Y %I:%M %p")
                
                status_change_reason = f'Order Item Created By - {order_item_created_by_qs.name} and Employee ID is {created_by} at {created_at_str}'
            
            status = 'ORDER_RECEIVED' 
            
            if order_type == 'POINT_OF_SELL':
                status = 'DELIVERED'
            else:
                status = 'ORDER_RECEIVED' 
              
            print(f"Barcode Number = {barcode_number}")
            
            product_stock_qs = None
            barcode_status = None
            
              
            if barcode_number:
                product_stock_qs = ProductStock.objects.filter(
                    barcode = barcode_number, status = "ACTIVE"
                ).last()
            
                # TODO 
                
                if not product_stock_qs:
                    order_qs.delete()
                    return ResponseWrapper(error_code=404, error_msg=f'{barcode_number}   is Not Found', status=404)
                
                elif product_stock_qs and not (product_stock_qs.status == "ACTIVE"):
                    order_qs.delete()
                    return ResponseWrapper(error_code=404, error_msg=f'{barcode_number}   is Not Active, This Barcode Current Status is {product_stock_qs.get_status_display()}', status=404)
                    
                barcode_status = product_stock_qs.status
            
            print('ggggggggggggggggg', selling_price)
            
            order_item_qs = order_item_create(
                barcode_status=barcode_status, order_item_qs=None, order_qs=order_qs,
                product_slug=product_slug, quantity=quantity, selling_price=selling_price,
                gsheba_amount=gsheba_amount, barcode_number = barcode_number,
                created_by=order_item_created_by, status_change_reason=status_change_reason, status=status
            )
            
            is_valid = order_item_qs.get('is_valid')
            error_msg = order_item_qs.get('error_msg')
            
            if not is_valid:
                logger.error("Order item creation failed: %s", error_msg)
                return ResponseWrapper(error_msg=error_msg, status=404)
        
        if order_payment_list:
            for order_payment in order_payment_list:
                transaction_no = order_payment.get('transaction_no')
                payment_method_slug = order_payment.get('payment_method_slug')
                received_amount = order_payment.get('received_amount')
                
                if payment_method_slug:
                    payment_qs = PaymentType.objects.filter(slug=payment_method_slug).last()
                    if not payment_qs:
                        logger.error("Payment method not found")
                        return ResponseWrapper(error_msg='Payment Method is Not Found', status=404)
                
                payment_slug = unique_slug_generator(name=order_qs.invoice_no) if name else None
                request_user = order_create_user
                order_status = order_qs.status
                status = 'RECEIVED'
                
                
                if payment_qs:
                    try:
                        slug = None
                        order_payment_log(slug, order_qs, payment_slug, payment_qs, order_status, received_amount, transaction_no, request_user, status)
                    except:
                        pass
                    
        
        order_status_slug = unique_slug_generator(name=order_qs.invoice_no) if name else None
        
        status_change_by = BaseSerializer(order_qs.created_by).data
        
        new_time = order_qs.created_at + timedelta(hours=6)
        
        created_at_str = new_time.strftime("%d %B, %Y %I:%M %p")
                
        status_change_reason = f'Order Item Created By - {request.user.email} at {created_at_str}'

        if employee_qs:
            status_change_reason = f'Order Created By - {employee_qs.name} and Employee ID is {employee_qs.employee_id}, at {created_at_str}'
        
        OrderStatusLog.objects.create(
            slug=order_status_slug,
            order=order_qs, status=order_qs.status,
            status_display=order_qs.get_status_display(),
            order_status_reason = status_change_reason,
            order_status_change_at=today,
            status_change_by=status_change_by,
            created_by=order_create_user
        )
        
        
        print(f'Before Pass order Create Serializer, Invoice No is = {order_qs.invoice_no}, Item ID is = {order_qs.order_items.all().last().id}, GSheba Amount ={order_qs.order_items.all().last().gsheba_amount}')
        
        qs = Order.objects.filter(invoice_no = order_qs.invoice_no).last()
        
        # serializer = OrderCreateSerializer(qs)
        
        calculate_order_price(qs)
        
        context = {
            'invoice_no': qs.invoice_no,
            'order_type': order_type,
            'order_date': qs.order_date
        }
        
        # if order_qs.order_type == "POINT_OF_SELL":
        #     order_payment_log_qs = OrderPaymentLog.objects.filter(order = order_qs)
            
        #     order_qs.total_payable_amount = sum(order_payment_log_qs.values_list('received_amount'), flat = True)
            
        #     order_qs.save()
            
        qs = Order.objects.filter(invoice_no = order_qs.invoice_no).last()
        
        if not order_type == "POINT_OF_SELL":
        
            try:
                # order_instance = order_qs
                
                subject = f"An Order {qs.get_order_type_display()} is Successfully Created"
                message_body = render_to_string('order/order_email_body.html', {'order_history_qs': qs})
                
                # message_body = f"<html><p> Dear Concern, </strong> <br> An Stock Transfer is Created By <strong>'{request.user.first_name} {request.user.last_name}' </strong>, And  The Transfer ID is  = #{invoice_no} at {order_qs.created_at}.</p>Thank you, <br> G-Projukti.com </html>"
                    
                send_email(email=email, subject= subject, body=message_body)
                
            except:
                pass
            
        
        return ResponseWrapper(data=context, msg='created', status=200)


    def order_details(self, request, invoice_no,  *args, **kwargs):
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        if order_qs.status in ["ORDER_RECEIVED", "PRODUCT_AVAILABILITY_CHECK"]:
            calculate_order_price(order_qs)
            
        # calculate_order_price(order_qs)
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        print(f"order_qs = {order_qs.total_payable_amount}")
            
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)


    def order_history_details_backup(self, request,  *args, **kwargs):
        order_qs = Order.objects.filter(order_type = "POINT_OF_SELL", invoice_no = "ONL0028600248")
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        order_item_list = order_qs.values_list('order_items', flat = True)       
        count = 1
        
        for order_item_id in order_item_list:
            order_item = OrderItem.objects.filter(id = order_item_id).last()
            
            rest_of = order_qs.count() - count
            
            print(f"count = {count}, Total =  {order_qs.count()}, Rest of = {rest_of}, order_item = {order_item}")
            count +=1
            
            product_qs = order_item.product
            
            print(f"Product = {product_qs}")
            
            product_warranty_list = product_qs.product_warrantys.all().order_by('warranty_type')
            
            
            
            for product_warranty in product_warranty_list:
                warranty_type = product_warranty.warranty_type
                warranty_duration = product_warranty.warranty_duration
                value = product_warranty.value
                
                print(f"Product Warranty Type = {warranty_type}")
                
                start_date = order_item.order.order_date
                
                print(f"Product Warranty Type = {warranty_type}, order_item.gsheba_amount ={order_item.gsheba_amount}")
                
                if warranty_type == "1_GSHEBA_WARRANTY" and order_item.gsheba_amount == 1:
                    pass
                
                else:
                    order_item_warranty_qs = order_item.order_item_warranty_logs.all().last()
                    
                    if order_item_warranty_qs:
                        start_date = order_item_warranty_qs.end_date
                        
                    if warranty_duration == 'DAY':
                        end_date = start_date + timedelta(days=int(value))
                    elif warranty_duration == 'MONTH':
                        end_date = start_date + timedelta(days=30 * int(value))  # Assuming 1 month = 30 days
                    elif warranty_duration == 'YEAR':
                        end_date = start_date + timedelta(days=365 * int(value)) 
                    
                    if order_item_warranty_qs:
                        order_item_warranty_log_qs = order_item.order_item_warranty_logs.filter(warranty_type = warranty_type)
                        if not order_item_warranty_log_qs:
                            order_item_warranty_qs = OrderItemWarrantyLog.objects.create(
                                order_item = order_item,
                                warranty_type = warranty_type,
                                warranty_duration = warranty_duration,
                                value = value,
                                start_date = start_date,
                                end_date = end_date,
                                created_by = order_item.created_by
                            )
                    elif not order_item_warranty_qs:
                        order_item_warranty_qs = OrderItemWarrantyLog.objects.create(
                                order_item = order_item,
                                warranty_type = warranty_type,
                                warranty_duration = warranty_duration,
                                value = value,
                                start_date = start_date,
                                end_date = end_date,
                                created_by = order_item.created_by
                            )
                
            
        
        # calculate_order_price(order_qs)
            
        order_qs = Order.objects.filter(invoice_no = 'ONL0028600248').last()
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    
    def courier_service_add_in_order(self, request, invoice_no,  *args, **kwargs):
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        courier_service_slug = request.data.get('courier_service_slug')
        
        if not courier_service_slug:
            return ResponseWrapper(error_msg='Courier Service Slug is Not Given', status=404)
        
        courier_service_qs = CourierService.objects.filter(slug = courier_service_slug).last()
        
        if not courier_service_qs:
            return ResponseWrapper(error_msg='Courier Service is Not Found', status=404)
        
        slug = unique_slug_generator(name = f"{invoice_no}-{courier_service_qs.name}")
        
        courier_service_qs = Courier.objects.create(
            order = order_qs,
            courier_service = courier_service_qs,
            courier_status = 'PENDING_PICKUP',
            slug = slug,
            created_by = request.user,
            )
        
        order_qs.status = 'DISPATCHED'
        order_qs.save()
        
        status_display = order_qs.get_status_display()
            
        today = TODAY 
        order_status_reason = f"Order Changed By {request.user}"
        status_change_by = BaseSerializer(request.user).data

        generate_order_status_log(
            order_obj= order_qs,
            status= 'DISPATCHED',
            status_display= status_display,
            order_status_reason = order_status_reason,
            status_change_by = status_change_by,
            order_status_change_at = today,
            created_by = request.user
            )
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)

    @log_activity
    def order_customer_info_address_update(self, request,invoice_no,  *args, **kwargs):
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        customer_address_qs = order_qs.customer_address_logs
        
        area_slug = request.data.get('area_slug')
        address = request.data.get('address') or order_qs.address
        address_type = request.data.get('address_type') or order_qs.customer_address_logs.last().address_type
        
        area_name =  order_qs.customer_address_logs.last().area_name
        district_name =  order_qs.customer_address_logs.last().district_name
        division_name =  order_qs.customer_address_logs.last().division_name
        country_name =  order_qs.customer_address_logs.last().country_name
        
        name = request.data.get('name') or order_qs.customer_address_logs.last().name
        phone = request.data.get('phone') or order_qs.customer_address_logs.last().phone
        email = request.data.get('email') or order_qs.customer_address_logs.last().email
        
        if area_slug:
            area_name = ''
            district_name = ''
            division_name = ''
            country_name = ''
            
            area_qs = Area.objects.filter(slug = area_slug).last()
        
            if not area_qs:
                return ResponseWrapper(error_msg='Area is Not Found', status=404)
            
            area_name = area_qs.name
            
            if area_qs.district:
                district_name = area_qs.district.name
                
            if area_qs.district.division:
                division_name = area_qs.district.division.name
                
            if area_qs.district.division.country:
                country_name = area_qs.district.division.country.name
                
            order_qs.area = area_qs
            order_qs.save()
            
        if address:
            order_qs.address = address
            order_qs.save()
            
            
        customer_address_qs = order_qs.customer_address_logs
        
        customer_address_qs.update(name = name, phone = phone, email = email,  address = address, area_name = area_name, district_name = district_name,  division_name = division_name, country_name = country_name,address_type = address_type, updated_by = request.user)
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)


    @log_activity
    def order_remarks(self, request, invoice_no, *args, **kwargs):
        try:
            order_qs = Order.objects.filter(invoice_no=invoice_no).last()
            if not order_qs:
                return ResponseWrapper(error_msg='Order is Not Found', status=404)
            
            remarks = request.data.get('remarks', None)

            if remarks is not None:
                order_qs.remarks = remarks
                order_qs.save()
                return ResponseWrapper(error_msg='Remarks Added Successfully', status=200)
            else:
                return ResponseWrapper(error_msg='Remarks field is required', status=400)
        
        except Exception as e:
            return ResponseWrapper(error_msg=str(e), status=500)



    @log_activity
    def order_status_update(self, request,invoice_no,  *args, **kwargs): 
        status = request.data.get('status')
        
        if request.data.get('order_status'):
            status = request.data.get('order_status')
            
        order_status_reason = request.data.get('order_status_reason') or None
        order_item_list = request.data.get('order_item_list')
        approved_status = request.data.get('approved_status')
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        try:
            if status and status == "DELIVERED":
                qs = EmployeeInformation.objects.filter(user = request.user, employee_id = "1360").last()
                
                if not qs:
                    return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' You haven't Permission for This Action '{status}' ", status=404)
                
                if order_qs.total_due_amount > 0:
                    return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' Due Amount is Not 0.0' ", status=404)
            
        except:
            pass
        
        if order_item_list:
            for order_item in order_item_list:
                order_item_id = order_item.get('order_item_id')
                
                product_slug = None
                order_item_qs = None
                
                # order_item_status = 'ORDER_RECEIVED'
                
                created_by = request.user
                status_change_reason = f"Order Status Changed By - {created_by.first_name} {created_by.last_name}"
                
                if order_item_id:
                    order_item_qs = OrderItem.objects.filter(id = order_item_id).last()
                    if not order_item_id:
                        return ResponseWrapper(error_msg='Order Item is Not Found', status=404)
                    
                    if order_item_qs.product:
                        product_slug = order_item_qs.product.slug
                    
                    
                    if order_item.get('status'):
                        order_item_status = order_item.get('status')
                    else:
                        order_item_status = order_item_qs.status
                        
                    if order_item.get('product_slug'):
                        product_slug = order_item.get('product_slug')
                    else:
                        product_slug = product_slug
                        
                    if order_item.get('quantity'):
                        quantity = order_item.get('quantity')
                    else:
                        quantity = order_item_qs.quantity
                        
                    if order_item.get('selling_price'):
                        selling_price = order_item.get('selling_price')
                    else:
                        selling_price = order_item_qs.selling_price
                        
                    if order_item.get('gsheba_amount'):
                        gsheba_amount = order_item.get('gsheba_amount')
                    else:
                        gsheba_amount = order_item_qs.gsheba_amount
                        
                    if order_item.get('barcode_number'):
                        barcode_number = order_item.get('barcode_number')
                    else:
                        barcode_number = order_item_qs.barcode_number
                    
                else:
                    product_slug = order_item.get('product_slug')
                    quantity = order_item.get('quantity')
                    selling_price = order_item.get('selling_price')
                    gsheba_amount = order_item.get('gsheba_amount')
                    barcode_number = order_item.get('barcode_number')
                    order_item_status = order_item.get('status')
                    
                if order_item_status in  ['CANCELLED'] and not order_status_reason:
                    return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' Status Change Reason is Mandatory when the Status is '{status}' ", status=404)
                
                if order_item_qs.status in ["CANCELLED", "RETURNED", "GSHEBA_RETURNED", "REFUNDED"]:
                    
                    pass
                
                else:
                    print(f"barcode_number= {barcode_number}")
                
                    if barcode_number == "-":
                        barcode_number = None
                        
                        
                    barcode_status =None
                    
                    if order_item_status in ['PACKAGED', "PACKAGED", "READY_FOR_PICKUP", "IN_TRANSIT", "DISPATCHED", "SHOP_DELIVERY_IN_TRANSIT", "DELIVERED_TO_CUSTOMER", "DELIVERED"]:
                        
                        barcode_status = "ACTIVE"
                    
                    # order_item_qs = order_item_create(barcode_status =None,order_item_qs= order_item_qs, order_qs = order_qs, product_slug = product_slug,quantity =  quantity, selling_price = selling_price, gsheba_amount = gsheba_amount, barcode_number = barcode_number, created_by = created_by, status = order_item_status, status_change_reason = status_change_reason)
                    
                    order_item_qs = order_item_create(barcode_status =barcode_status,order_item_qs= order_item_qs, order_qs = order_qs, product_slug = product_slug,quantity =  quantity, selling_price = selling_price, gsheba_amount = gsheba_amount, barcode_number = barcode_number, created_by = created_by, status = order_item_status, status_change_reason = status_change_reason)
                    
                    calculate_order_price(order_qs)
                
                    is_valid = order_item_qs.get('is_valid')
                    error_msg = order_item_qs.get('error_msg')
                    
                    if not is_valid:
                        return ResponseWrapper(error_msg=error_msg, status=404) 
                
        profile_image_url = None
            
        user_information_qs =  UserInformation.objects.filter(user = request.user).last()
        if user_information_qs:
            profile_image_url = user_information_qs.image
            
            status_change_by = BaseSerializer(request.user).data
            
        if status:
            print(f'Before status = {order_qs.status}, Request Status = {status}')
            
            order_status_log_qs = OrderStatusLog.objects.filter(order__invoice_no = order_qs.invoice_no)
            
            if order_status_log_qs:
                return_order_log_qs = order_status_log_qs.filter(status='RETURNED')
                
                if not return_order_log_qs:
                    order_status_log_qs = order_status_log_qs.filter(status='RETURNED').filter(status = status).last()
                
                    if order_status_log_qs:
                        return ResponseWrapper(error_msg=f"#{invoice_no} Order Status is Already in '{order_status_log_qs.status_display}'", status=400)
                
            if status in  ['CANCELLED'] and not order_status_reason:
                return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' Status Change Reason is Mandatory when the Status is '{status}' ", status=404)
            
            order_qs.status = status
            order_qs.save()
            
            print(f'After status = {order_qs.status}')
            
            if not order_item_list:
                
                order_item_qs = order_qs.order_items.filter(status = status)
                
                order_item_qs.update(status = status)
            
            serializer = OrderDetailsSerializer(instance=order_qs)
            
            order_info_data = serializer.data
        
            status_display = order_info_data['status_display']
            
            today = TODAY 

            generate_order_status_log(
                order_obj= order_qs,
                status= status,
                status_display= status_display,
                order_status_reason = order_status_reason,
                status_change_by = status_change_by,
                order_status_change_at = today,
                created_by = request.user
                )
            
            if status in  ['WAREHOUSE_TO_SERVICE_POINT', "WAREHOUSE_TO_VENDOR"]:
                last_service_order_qs = ServicingOrder.objects.all().order_by('-created_at').last()
                if last_service_order_qs:
                    last_invoice_no = last_service_order_qs.invoice_no
                else:
                    last_invoice_no = 'SER000000001'
                    
                invoice_no = generate_service_invoice_no(last_invoice_no)
        
                service_order_create_or_update(invoice_no= invoice_no,servicing_type = 'ORDER', order = order_qs, request_user = request.user, status = 'WAREHOUSE_TO_SERVICE_POINT', order_date = today)

            # this have to test
            try:
                order_history_qs = Order.objects.filter(invoice_no=invoice_no).last()
                customer_email = order_history_qs.customer.user.email

                # if not customer_email:
                #     return  # Exit function if customer email is not available
                # have to change mail
                customer_and_accounts_mail = [customer_email, "gr.audit@kbg.com.bd", "babul.hosen@kbg.com.bd", "setusakilanasrin@gmail.com"]  # Placeholder, adjust as needed
                
                customer_and_accounts_mail.append(customer_email)
                
                # print(customer_and_accounts_mail, 'all mail')
                
                status = order_history_qs.status
                subject = f"Your order status is {order_history_qs.get_status_display()}"
                
                message_body = render_to_string('order/order_status_update.html', {'order_history_qs': order_history_qs})
                # change with accounts mail
                if status == 'DELIVERED':
                    send_email(email=customer_email, subject=subject, body=message_body)

                if status == 'DELIVERED_TO_CUSTOMER':
                    for mail in customer_and_accounts_mail:
                        send_email(email=mail, subject=subject, body=message_body)

            except Order.DoesNotExist:
                # Handle the case where order history with the given ID does not exist
                pass
            except Exception as e:
                # Handle any other exceptions that might occur (e.g., email sending failure)
                print(f"Failed to send order status email: {e}")


        if approved_status:
            order_qs.approved_status = approved_status
            order_qs.save()
            
            order_status_log_qs = OrderStatusLog.objects.filter(
                order__invoice_no = invoice_no, status = approved_status
            )
            order_approved_status_display =  order_qs.approved_status.get_approved_status_display()
            
            if not order_status_log_qs:

                created_at_str = settings.TODAY.strftime("%d %B, %Y %I:%M %p")
                
                order_status_reason = f"Order Change By {request.user} at {created_at_str}"
                
                employee_qs = EmployeeInformation.objects.filter(user = request.user).last()
                
                if employee_qs:
                    order_status_reason = f'Order Created By - {employee_qs.name} and Employee ID is {employee_qs.employee_id}, at {created_at_str}'
                    
                status_log_slug = unique_slug_generator(name=order_qs.invoice_no) if order_qs.invoice_no else None
    
                order_status_log_qs = OrderStatusLog.objects.create(
                    slug = status_log_slug,
                    order = order_qs,
                    status = approved_status,
                    status_display = order_approved_status_display,
                    order_status_reason = order_status_reason,
                    status_change_by = status_change_by,
                    order_status_change_at = today,
                    created_by = request.user
                )
            # send mail
            try:
                order_history_qs = Order.objects.filter(invoice_no=invoice_no).last()
                customer_email = order_history_qs.customer.user.email

                customer_and_accounts_mail = customer_email
                
                status = order_history_qs.status
                subject = f"Your order status is {order_history_qs.get_status_display()}"
                
                message_body = render_to_string('order/order_status_update.html', {'order_history_qs': order_history_qs})
                # change with accounts mail
                send_email(email=customer_and_accounts_mail, subject=subject, body=message_body)

            except Order.DoesNotExist:
                # Handle the case where order history with the given ID does not exist
                pass
            except Exception as e:
                # Handle any other exceptions that might occur (e.g., email sending failure)
                print(f"Failed to send approve status email: {e}")

        try:
            channel_layer = get_channel_layer()
            
            group_name = f'admin-panel-{request.user.id}'
            
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification',
                    'data': f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()}"
                    # 'order': serializer.data
                }
            )
            logger.info(f'Notification sent for user {request.user.id} with order data: {serializer.data}')
            
            print('Success')
            
            created_date_str = order_qs.created_at.strftime('%d %B, %Y at %I:%M %p')
            
            user_notification_qs = UserNotification.objects.create(
                    title = f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()}",
                    description=f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()} By {request.user.email} at {created_date_str}",
                    created_by = order_qs.updated_by, user_information= request.user
                )
            
            print('ooooooooooooo')
            
        except Exception as e:
            logger.error(f'Error sending notification: {e}')
            
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    
    
    @log_activity
    def order_return_status_update(self, request,invoice_no,  *args, **kwargs):
        status = request.data.get('status')
        order_status_reason = request.data.get('order_status_reason') or None
        refunded_account_holder_name = request.data.get('refunded_account_holder_name') or None
        refunded_account_number = request.data.get('refunded_account_number') or None
        order_item_list = request.data.get('order_item_list')
        approved_status = request.data.get('approved_status')
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        # if not order_qs.status in ['DELIVERED', 'CANCELLED', 'RETURNED', 'GSHEBA_RETURNED', 'REFUNDED', 'DELIVERED_TO_CUSTOMER']:
            
        #     return ResponseWrapper(error_msg=f'{invoice_no}, Order is Not Ready for Return', status=404)
        
        if order_qs.status == status:
            return ResponseWrapper(error_msg=f'This Order is Already in {order_qs.get_status_display()}', status=404)
        
        profile_image_url = None
            
        user_information_qs =  UserInformation.objects.filter(user = request.user).last()
        if user_information_qs:
            profile_image_url = user_information_qs.image
            
            status_change_by = BaseSerializer(request.user).data
        today = TODAY
        
        if not order_item_list:
            order_item_list = order_qs.order_items.all()
        
        if approved_status:
            if approved_status in ['REJECTED'] and not order_status_reason:
                return ResponseWrapper(error_msg='Reject Change Reason is Mandatory', status=404) 
            
            
            order_qs.approved_status = approved_status
            order_qs.save()
            
            order_status_log_qs = OrderStatusLog.objects.filter(
                order__invoice_no = invoice_no, status = approved_status
            )
            
            if not order_status_log_qs:
                
                order_approved_status_display =  order_qs.get_approved_status_display()
                
                if not order_status_reason:
                    order_status_reason = f"Order {order_approved_status_display} By {request.user}"
                else:
                    order_status_reason = order_status_reason
                
                status_log_slug = unique_slug_generator(name=order_qs.invoice_no) if order_qs.invoice_no else None
                
                order_status_log_qs = OrderStatusLog.objects.create(
                    slug = status_log_slug,
                    order = order_qs,
                    status = approved_status,
                    status_display = order_approved_status_display,
                    order_status_reason = order_status_reason,
                    status_change_by = status_change_by,order_status_change_at = today,
                    created_by = request.user
                )
            
        
        for order_item in order_item_list:
            try:
                order_item_id = order_item.get('order_item_id')
                status_change_reason = order_item.get('status_change_reason')
            except:
                order_item_id = order_item.id
                status_change_reason = None
            
            product_slug = None
            order_item_qs = None
            quantity = 1
            selling_price = None
            
            created_by = request.user
            
            if not order_item_id:
                return ResponseWrapper(error_msg='Order id Not Found', status=404)
            
            if not status_change_reason:
                status_change_reason = f"Order Status Change to {order_qs.get_status_display()}, and  Changed By - {created_by.first_name} {created_by.last_name} at {TODAY.strftime('%b %d, %Y at %I:%M %p')}"
                
            else:
                status_change_reason = status_change_reason
                
            if order_item_id:
                order_item_qs = OrderItem.objects.filter(id = order_item_id).last()
                if not order_item_qs:
                    return ResponseWrapper(error_msg='Order Item is Not Found', status=404)
                
                product_slug = order_item_qs.product.slug if order_item_qs.product else None
                quantity = order_item.get('quantity', order_item_qs.quantity)
                selling_price = order_item.get('selling_price', order_item_qs.selling_price)
                gsheba_amount = order_item.get('gsheba_amount', order_item_qs.gsheba_amount)
                barcode_number = order_item.get('barcode_number', order_item_qs.barcode_number)
                order_item_status = order_item.get('status', order_item_qs.status)
                
                print(f"order_qs.status = {order_qs.status} and Item Status = {order_item_status}")
                
                
                if order_qs.status == 'GSHEBA_RETURNED':
                    
                    barcode_status = "GSHEBA_FAUlLY"
                    
                else:
                    barcode_status = order_item.get('barcode_status', order_item_qs.barcode_status)

            
            if order_item_status in ['RETURNED', 'GSHEBA_RETURNED'] and barcode_number:
                
                product_stock_qs = ProductStock.objects.filter(barcode = barcode_number).last()
                
                if not product_stock_qs:
                    return ResponseWrapper(error_msg='Barcode is not Found', status=404)
                
                
            order_item_qs = order_item_create(barcode_status=barcode_status, order_item_qs= order_item_qs, order_qs = order_qs, product_slug = product_slug,barcode_number = barcode_number, created_by = created_by, status = order_item_status, status_change_reason = status_change_reason,quantity=quantity, selling_price=selling_price, gsheba_amount=gsheba_amount)
             
            is_valid = order_item_qs.get('is_valid')
            error_msg = order_item_qs.get('error_msg')
            
            if not is_valid:
                return ResponseWrapper(error_msg=error_msg, status=404) 
            
        profile_image_url = None
            
        user_information_qs =  UserInformation.objects.filter(user = request.user).last()
        if user_information_qs:
            profile_image_url = user_information_qs.image
            
            status_change_by = BaseSerializer(request.user).data
        if status:
            order_status_log_qs = OrderStatusLog.objects.filter(order__invoice_no = order_qs.invoice_no)
            
            if status in  ['RETURNED', 'GSHEBA_RETURNED', 'CANCELLED'] and not order_status_reason:
                return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' Status Change Reason is Mandatory when the Status is '{status}' ", status=404)
            
            today = TODAY
            
            warranty_valid_qs = order_qs.order_items.filter(order_item_warranty_logs__end_date__gte = today, order_item_warranty_logs__warranty_type = '1_GSHEBA_WARRANTY')
            
            if warranty_valid_qs:
                status = 'GSHEBA_RETURNED'
            else:
                status = status
                
            order_qs.status = status
            order_qs.save()
            
            if order_qs.status in ['RETURNED', 'GSHEBA_RETURNED']:
                order_qs.approved_status == 'INITIALIZED'
                order_qs.save()
                
            serializer = OrderDetailsSerializer(instance=order_qs)
            
            order_info_data = serializer.data
        
            status_display = order_info_data['status_display']
            
            today = TODAY 

            generate_order_status_log(
                order_obj= order_qs,
                status= status,
                status_display= status_display,
                order_status_reason = order_status_reason,
                status_change_by = status_change_by,
                order_status_change_at = today,
                created_by = request.user
                )
        
                
        if refunded_account_holder_name:
            order_qs.refunded_account_holder_name = refunded_account_holder_name
        if refunded_account_number:
            order_qs.refunded_account_number = refunded_account_number
            
        order_qs.save()
            
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)

    @log_activity
    def apply_promo_code(self, request, invoice_no,  *args, **kwargs):
        promo_code = request.data.get('promo_code')

        order_instance = Order.objects.filter(
            invoice_no=invoice_no
        ).last()

        if not order_instance:
            return ResponseWrapper(error_msg='Order Not Found', error_code=404)
        
        print("Gggggggggg", promo_code)
        
        promo_qs = PromoCode.objects.filter(
            promo_code=promo_code
        ).last()

        if not promo_qs:
            return ResponseWrapper(error_msg='Promo Code is Not Found', error_code=404)

        order_instance.promo_code = promo_code
        order_instance.save()
        
        price_details = calculate_order_price(order_obj = order_instance)
        
        serializer = OrderDetailsSerializer(order_instance)
        return ResponseWrapper(data=serializer.data, status=200, msg='Promo Applied Successfully')
    
    
    @log_activity
    def order_return_status_approved_rejected(self, request,invoice_no,  *args, **kwargs):
        approved_status = request.data.get('approved_status')
        status_change_reason = request.data.get('status_change_reason')
        
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        if not order_qs.status in ['RETURNED', 'GSHEBA_RETURNED', 'REFUNDED', 'DELIVERED_TO_CUSTOMER']:
            
            return ResponseWrapper(error_msg='This Order is Not Ready for Return', status=404)
        
        profile_image_url = None
            
        user_information_qs =  UserInformation.objects.filter(user = request.user).last()
        if user_information_qs:
            profile_image_url = user_information_qs.image
            
            status_change_by = BaseSerializer(request.user).data
            
        today = TODAY
        
        order_item_list = order_qs.order_items.all()
        
        if approved_status:
            if approved_status in ['REJECTED'] and not status_change_reason:
                return ResponseWrapper(error_msg='Reject Change Reason is Mandatory', status=404) 
            
            
            order_qs.approved_status = approved_status
            order_qs.save()
            
            order_status_log_qs = OrderStatusLog.objects.filter(
                order__invoice_no = invoice_no, status = approved_status
            )
            
            if not order_status_log_qs:
                
                order_approved_status_display =  order_qs.get_approved_status_display()
                
                if not status_change_reason:
                    status_change_reason = f"Order {order_approved_status_display} By {request.user}"
                else:
                    status_change_reason = status_change_reason
                
                status_log_slug = unique_slug_generator(name=order_qs.invoice_no) if order_qs.invoice_no else None 
                
                order_status_log_qs = OrderStatusLog.objects.create(
                    slug = status_log_slug,
                    order = order_qs,
                    status = approved_status,
                    status_display = order_approved_status_display,
                    order_status_reason = status_change_reason,
                    status_change_by = status_change_by,order_status_change_at = today,
                    created_by = request.user
                )
            
        
        for order_item in order_item_list:
            created_by = request.user
            
            if not status_change_reason:
                status_change_reason = f"Order Status Changed By - {created_by.first_name} {created_by.last_name} "
                
            else:
                status_change_reason = status_change_reason
                
            order_item_qs = OrderItem.objects.filter(id = order_item.id).last()
            if not order_item_qs:
                return ResponseWrapper(error_msg='Order Item is Not Found', status=404)
            
            product_slug = order_item_qs.product.slug if order_item_qs.product else None
            quantity = order_item_qs.quantity
            selling_price = order_item_qs.selling_price
            gsheba_amount = order_item_qs.gsheba_amount
            barcode_number = order_item_qs.barcode_number
            order_item_status = order_item_qs.status
            barcode_status = order_item_qs.barcode_status
            
            if order_item_qs.status == "GSHEBA_RETURNED":
                barcode_status = "GSHEBA_FAUlLY"
     
            order_item_qs = order_item_create(barcode_status=barcode_status, order_item_qs= order_item_qs, order_qs = order_qs, product_slug = product_slug,barcode_number = barcode_number, created_by = created_by, status = order_item_status, status_change_reason = status_change_reason,quantity=quantity, selling_price=selling_price, gsheba_amount=gsheba_amount)
            
            if order_item_status in ['RETURNED', 'GSHEBA_RETURNED'] and barcode_number:
                
                product_stock_qs = ProductStock.objects.filter(barcode = barcode_number).last()
                
                if not product_stock_qs:
                    return ResponseWrapper(error_msg='Barcode is not Found', status=404)
             
            is_valid = order_item_qs.get('is_valid')
            error_msg = order_item_qs.get('error_msg')
            
            if not is_valid:
                return ResponseWrapper(error_msg=error_msg, status=404) 
            
        profile_image_url = None
            
        user_information_qs =  UserInformation.objects.filter(user = request.user).last()
        if user_information_qs:
            profile_image_url = user_information_qs.image
            
            status_change_by = BaseSerializer(request.user).data
            
        if approved_status:
            order_qs.approved_status = approved_status
            order_qs.save()
            
            order_status_log_qs = OrderStatusLog.objects.filter(
                order__invoice_no = invoice_no, status = approved_status
            )
            order_approved_status_display =  order_qs.get_approved_status_display()
            
            if not order_status_log_qs:
                status_change_reason = f"Order Approved By {request.user}"
                
                status_log_slug = unique_slug_generator(name=order_qs.invoice_no) if order_qs.invoice_no else None
    
                order_status_log_qs = OrderStatusLog.objects.create(
                    slug = status_log_slug,
                    order = order_qs,
                    status = approved_status,
                    status_display = order_approved_status_display,
                    order_status_reason = status_change_reason,
                    status_change_by = status_change_by,order_status_change_at = today,
                    created_by = request.user
                )
                
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    

    @log_activity
    def gsheba_return_item_add(self, request,invoice_no,  *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True, many = True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        request_data_list = request.data
        for order_item in request_data_list:
            order_item_id = order_item.get('order_item_id') or None
            quantity = order_item.get('quantity') or 1
            status = order_item.get('status') or None
            product_slug = order_item.get('product_slug')
            selling_price = order_item.get('selling_price') or 0.0
            gsheba_amount = order_item.get('gsheba_amount') or 0.0
            barcode_number = order_item.get('barcode_number')
            status_change_reason = order_item.get('status_change_reason')
            created_by = request.user
            order_item_qs = None
            
            barcode_status = None
            order_item_qs = order_item_create(barcode_status = "FAULTY", order_item_qs= None, order_qs = order_qs, product_slug = product_slug,quantity =  quantity, selling_price = selling_price, gsheba_amount = gsheba_amount, barcode_number = barcode_number, created_by = created_by, status_change_reason = status_change_reason, status='DELIVERED')
        
        
            serializer = OrderDetailsSerializer(instance=order_qs)
            
            order_info_data = serializer.data
        
            status_display = order_info_data['status_display']
            
            profile_image_url = None
            
            user_information_qs =  UserInformation.objects.filter(user = request.user).last()
            if user_information_qs:
                profile_image_url = user_information_qs.image
                
                status_change_by = BaseSerializer(request.user).data
            today = TODAY 
            
            order_status_reason = 'Order Created By {user_information_qs.name}'

            generate_order_status_log(
                order_obj= order_qs,
                status= order_qs.status,
                status_display= status_display,
                order_status_reason = order_status_reason,
                status_change_by = status_change_by,
                order_status_change_at = today,
                created_by = request.user
                )
        
        order_qs.status = 'DELIVERED'
        order_qs.save()
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
            
        
    @log_activity
    def order_item_update(self, request,invoice_no,  *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True, many = True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        request_data_list = request.data
        
        for order_item in request_data_list:
            order_item_id = order_item.get('order_item_id') or None
            quantity = order_item.get('quantity') or None
            status = order_item.get('status') or None
            product_slug = order_item.get('product_slug')
            selling_price = order_item.get('selling_price') or 0.0
            gsheba_amount = order_item.get('gsheba_amount') or 0.0
            barcode_number = order_item.get('barcode_number')
            status_change_reason = order_item.get('status_change_reason')
            
            parent_order_item_id = None
            
            if order_item.get('parent_order_item_id'):
                parent_order_item_id = order_item.get('parent_order_item_id')
            
            created_by = request.user
            order_item_qs = None
            
            if status in  ['CANCELLED', 'RETURNED'] and not status_change_reason:
                
                return ResponseWrapper(error_msg=f"For Order Item ID = '{order_item_id}' Status Change Reason is Mandatory when the Status is '{status}' ", status=404)
            
            if order_item_id:
                order_item_qs = OrderItem.objects.filter(id = order_item_id).last()
                
                if not order_item_qs:
                    return ResponseWrapper(error_msg='Order Item is Not Found', status=404)
                
            barcode_status = None
            order_item_qs = order_item_create(barcode_status,order_item_qs, order_qs, product_slug, quantity, selling_price, gsheba_amount, barcode_number, created_by, status, status_change_reason)
            
            if parent_order_item_id:
                order_item_qs.order_item_id = parent_order_item_id
                order_item_qs.is_gift_item = True
                order_item_qs.save()
        
        
            serializer = OrderDetailsSerializer(instance=order_qs)
            
            order_info_data = serializer.data
        
            status_display = order_info_data['status_display']
            
            profile_image_url = None
            
            user_information_qs =  UserInformation.objects.filter(user = request.user).last()
            if user_information_qs:
                profile_image_url = user_information_qs.image
                
                status_change_by = BaseSerializer(request.user).data
                
            today = TODAY 
            
            order_status_reason = 'Order Created By {user_information_qs.name}'

            generate_order_status_log(
                order_obj= order_qs,
                status= order_qs.status,
                status_display= status_display,
                order_status_reason = order_status_reason,
                status_change_by = status_change_by,
                order_status_change_at = today,
                created_by = request.user
                )
            
        calculate_order_price(order_qs)
        
        order_qs = Order.objects.filter(invoice_no = order_qs.invoice_no).last()
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    
    @log_activity
    def order_item_remove(self, request,order_item_id, *args, **kwargs):
        order_item_qs = OrderItem.objects.filter(id = order_item_id).last()

        if not order_item_qs:
            return ResponseWrapper(error_msg='Order Item is Not Found', status=404)
        
        order_qs = Order.objects.filter(invoice_no = order_item_qs.order.invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        order_item_qs.delete()
        
        calculate_order_price(order_qs)
        order_qs = Order.objects.filter(invoice_no = order_item_qs.order.invoice_no).last()
        
        # activity_log(order_item_qs, request,serializer=None)
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Order Item Deleted Successfully', status=200)
    
    
    @log_activity
    def order_payment_log_remove(self, request,slug, *args, **kwargs):
        order_payment_log_qs = OrderPaymentLog.objects.filter(slug = slug).last()

        if not order_payment_log_qs:
            return ResponseWrapper(error_msg='Order Payment Log is Not Found', status=404)
        
        order_qs = Order.objects.filter(invoice_no = order_payment_log_qs.order.invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        order_payment_log_qs.delete()
        activity_log(order_payment_log_qs, request,serializer=None)
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Order Payment Log Deleted Successfully', status=200)
    
    
    @log_activity
    def order_payment_log_update(self, request, invoice_no, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True, many = True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        order_payment_list = request.data
        
        payment_method_slugs = [item['payment_method_slug'] for item in order_payment_list]
        
        order_payment_log_delete_qs = OrderPaymentLog.objects.exclude(order_payment__slug__in=payment_method_slugs).filter(order__invoice_no = invoice_no)
        
        order_payment_log_delete_qs.delete()


        
        for order_payment in order_payment_list:
            slug = None
            
            try:
                slug = order_payment.get('slug')
            except:
                slug = None
                
            transaction_no = order_payment.get('transaction_no')
            payment_method_slug = order_payment.get('payment_method_slug')
            received_amount = order_payment.get('received_amount')
            
            if payment_method_slug:
                payment_qs =  PaymentType.objects.filter(
                    slug = payment_method_slug
                ).last()
                
                if not payment_qs:
                    return ResponseWrapper(error_msg='Payment Method is Not Found', status=404)
                
            order_payment_qs = OrderPaymentLog.objects.filter(
                slug = slug,
                order = order_qs, order_payment = payment_qs, received_amount = received_amount).last()
            
            if order_payment_qs:
                payment_slug = order_payment_qs.slug
                
            else:
                payment_slug = unique_slug_generator(name=f"{order_qs.invoice_no}-{payment_qs.name}") if order_qs.invoice_no else None
            
            request_user = request.user
            
            order_status = order_qs.status
            status = 'RECEIVED'
            
            order_payment_log(slug, order_qs, payment_slug, payment_qs, order_status, received_amount, transaction_no, request_user, status)
            
        
        order_payment_log_qs = OrderPaymentLog.objects.filter(order = order_qs, status = "RECEIVED")
        
        total_received_amount = sum(order_payment_log_qs.values_list('received_amount', flat =  True))
        
        total_due_amount = order_qs.total_payable_amount - total_received_amount
        
        order_qs.total_paid_amount = total_received_amount
        order_qs.total_due_amount = total_due_amount
        order_qs.save()
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Payment Add Successfully', status=200)
        
    @log_activity
    def order_refunded_payment_update(self, request, invoice_no, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True, many = True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        order_payment_list = request.data
        
        for order_payment in order_payment_list:
            transaction_no = order_payment.get('transaction_no')
            payment_method_slug = order_payment.get('payment_method_slug')
            received_amount = order_payment.get('received_amount')
            
            if payment_method_slug:
                payment_qs =  PaymentType.objects.filter(
                    slug = payment_method_slug
                ).last()
                
                if not payment_qs:
                    return ResponseWrapper(error_msg='Payment Method is Not Found', status=404)
                
            payment_slug = unique_slug_generator(name=order_qs.invoice_no) if order_qs.invoice_no else None
            
            request_user = request.user
            
            order_status = order_qs.status
            status = "REFUNDED"
            
            slug = None
            
            order_payment_log(slug, order_qs, payment_slug, payment_qs, order_status, received_amount, transaction_no, request_user, status)
            
        order_qs.status ='REFUNDED'
        order_qs.save()
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Payment Refunded Add Successfully', status=200)
        

    @log_activity
    def order_item_status_log(self, request, order_item_id, *args, **kwargs):
        order_item_status_log_qs = OrderItemStatusLog.objects.filter(order_item__pk = order_item_id).order_by('-id')
        
        serializer = OrderItemStatusLogListSerializer(instance=order_item_status_log_qs, many = True)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
        
    @log_activity
    def order_invoice_print(self, request, invoice_no, *args, **kwargs):
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        context = {
            'order_data': serializer.data,
        }
        
        pdf= render_to_pdf('order/order-invoice.html',context)
        if pdf:
            response=HttpResponse(pdf, content_type="application/pdf")
            
            # ....***.... Show PDF File ....***....
            content="inline; filename=voucher.pdf" 
            # ....***.... Automated Download PDF File ....***....
            
            # content="attachment; filename=voucher.pdf"
            response['Content-Disposition']=content
            
        return response
    
    @log_activity
    def order_invoice_label_print(self, request, invoice_no, *args, **kwargs):
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        context = {
            'order_data': serializer.data,
        }
        
        pdf= render_to_pdf('order/order-label.html',context)
        if pdf:
            response=HttpResponse(pdf, content_type="application/pdf")
            
            # ....***.... Show PDF File ....***....
            # content="inline; filename=voucher.pdf" 
            # ....***.... Automated Download PDF File ....***....
            
            content="attachment; filename=voucher.pdf"
            response['Content-Disposition']=content
            
        return response 
    
    
    @log_activity
    def multiple_order_invoice_print(self, request, *args, **kwargs):
        invoice_list = request.data
        max_workers = min(8, len(invoice_list))  # Adjust dynamically based on input size

        def process_order(invoice_no):
            try:
                order_qs = Order.objects.filter(invoice_no=invoice_no).last()
                if not order_qs:
                    return invoice_no, None
                serializer = OrderDetailsSerializer(instance=order_qs)
                context = {'order_data': serializer.data}
                return invoice_no, render_to_pdf('order/order-invoice.html', context)
            except Exception as e:
                logger.error(f'Error processing order {invoice_no}: {str(e)}')
                return invoice_no, None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_order, order['invoice_no']): order['invoice_no'] 
                       for order in invoice_list}
            
            pdf_results = {}
            invoices_not_found = []
            
            for future in as_completed(futures):
                invoice_no = futures[future]
                try:
                    result_invoice_no, pdf_content = future.result()
                    if pdf_content:
                        pdf_results[result_invoice_no] = pdf_content
                    else:
                        invoices_not_found.append(result_invoice_no)
                except Exception as e:
                    logger.error(f'Error with future result for invoice {invoice_no}: {str(e)}')
                    invoices_not_found.append(invoice_no)

        if invoices_not_found:
            return Response({'error_msg': f'Invoices not found: {invoices_not_found}'}, status=404)

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for invoice_no, pdf_content in pdf_results.items():
                zip_file.writestr(f'Order-Invoice-{invoice_no}.pdf', pdf_content)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="Order-Invoices.zip"'
        return response
    
    
    
    @log_activity
    def multiple_order_label_print(self, request, *args, **kwargs):
        invoice_list = request.data
        max_workers = min(8, len(invoice_list))  # Adjust dynamically based on input size

        def process_order(invoice_no):
            try:
                order_qs = Order.objects.filter(invoice_no=invoice_no).last()
                if not order_qs:
                    return invoice_no, None
                serializer = OrderDetailsSerializer(instance=order_qs)
                context = {'order_data': serializer.data}
                return invoice_no, render_to_pdf('order/order-label.html', context)
            except Exception as e:
                logger.error(f'Error processing order {invoice_no}: {str(e)}')
                return invoice_no, None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_order, order['invoice_no']): order['invoice_no'] 
                       for order in invoice_list}
            
            pdf_results = {}
            invoices_not_found = []
            
            for future in as_completed(futures):
                invoice_no = futures[future]
                try:
                    result_invoice_no, pdf_content = future.result()
                    if pdf_content:
                        pdf_results[result_invoice_no] = pdf_content
                    else:
                        invoices_not_found.append(result_invoice_no)
                except Exception as e:
                    logger.error(f'Error with future result for invoice {invoice_no}: {str(e)}')
                    invoices_not_found.append(invoice_no)

        if invoices_not_found:
            return Response({'error_msg': f'Invoices not found: {invoices_not_found}'}, status=404)

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for invoice_no, pdf_content in pdf_results.items():
                zip_file.writestr(f'Order-Invoice-Label-{invoice_no}.pdf', pdf_content)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="Order-Label-Invoices.zip"'
        return response
    
    @log_activity
    def pos_invoice_print(self, request,invoice_no, *args, **kwargs):

        from django.template.loader import render_to_string
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', error_code=404)
        
        serializer = OrderDetailsSerializer(
            instance=order_qs)
        
        now = datetime.now()
        order_details_serializer = serializer.data
        
        order_item_list = order_details_serializer.get('order_items_details')
        customer_details = order_details_serializer.get('customer_details')
        customer_address_details = order_details_serializer.get('customer_address_details')
         
        
        context = {
            'order_id': invoice_no,
            'customer_details': customer_details,
            'customer_address_details': customer_address_details,
            'order_date': order_qs.order_date,
            'time': str(now.strftime("%I:%M %p")),
            'items_data': order_item_list,
            'total_tax_amount': order_qs.total_tax_amount,
            'total_product_price': order_qs.total_product_price,
            'total_promo_discount': order_qs.total_promo_discount,
            'total_payable_amount': order_qs.total_payable_amount,
        }
        try: 
            html_string = render_to_string('order/invoice.html', context)
            
            # css_string = '@page { size: 1070mm; margin: 0mm }'
            # pdf_file = HTML(string=html_string).write_pdf(stylesheets=[CSS(string=css_string)])
            
            # pdf_file = HTML(string=html_string).write_pdf()
            pdf_file = render_to_string('order/invoice.html', context)
    
            if pdf_file:
                return HttpResponse(html_string, content_type="text/html")
            
        except Exception as e:
            return ResponseWrapper(error_msg=str(e), error_code=400)
            # print('Error generating PDF:', e)

    @log_activity
    def return_pos_invoice_print(self, request, invoice_no, *args, **kwargs):
        from django.template.loader import render_to_string
        order_qs = Order.objects.filter(
            invoice_no = invoice_no
        ).last()

        if not order_qs:
            return ResponseWrapper(
                error_msg='Return order is Not Found', error_code=404)

        serializer = OrderDetailsSerializer(
            instance=order_qs)

        now = datetime.now()
        order_details_serializer = serializer.data
        order_item_list = order_details_serializer.get('order_items_details')
        customer_details = order_details_serializer.get('customer_details')
        customer_address_details = order_details_serializer.get(
            'customer_address_details'
        )

        context = {
            'order_id': invoice_no,
            'customer_details': customer_details,
            'customer_address_details': customer_address_details,
            'order_date': order_qs.order_date,
            'time': str(now.strftime("%I:%M %p")),
            'items_data': order_item_list,
            'total_tax_amount': order_qs.total_tax_amount,
            'total_product_price': order_qs.total_product_price,
            'total_promo_discount': order_qs.total_promo_discount,
            'total_payable_amount': order_qs.total_payable_amount,
        }
        try:
            html_string = render_to_string('order/return_invoice_print.html', context)
            pdf_file = render_to_string('order/return_invoice_print.html', context)
            if pdf_file:
                return HttpResponse(html_string, content_type="text/html")
        except Exception as e:
            return ResponseWrapper(error_msg=str(e), error_code=400)
        
class ServiceOrderViewSet(CustomViewSet):
    queryset = ServicingOrder.objects.all().order_by('-order_date')
    lookup_field = 'invoice_no'
    serializer_class = ServiceOrderListSerializer
    permission_classes = [CheckCustomPermission]
    
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.OrderingFilter,
    # )
    # filterset_class = OrderFilter
    
    def get_serializer_class(self):
        if self.action in ['service_order_status_update']:
            self.serializer_class = OrderStatusUpdateSerializer
        elif self.action in ['list']:
            self.serializer_class = ServiceOrderListSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = ServiceOrderDetailsSerializer
        else:
            self.serializer_class = ServiceOrderListSerializer

        return self.serializer_class
    
    @log_activity
    def retrieve(self, request,invoice_no,  *args, **kwargs):
        service_order_qs = ServicingOrder.objects.filter(invoice_no = invoice_no).last()
        
        if not service_order_qs:
            return ResponseWrapper(error_msg='Service Order is Not Found', status=404)
        
        # order_qs = Order.objects.filter(service_no = invoice_no).last()
        
        serializer = ServiceOrderDetailsSerializer(instance=service_order_qs)
        # serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    
    @log_activity
    def service_order_status_update(self, request,invoice_no,  *args, **kwargs):
        status = request.data.get('status')
        order_status_reason = request.data.get('order_status_reason') or None
        service_order_item_list = request.data.get('service_order_item_list')
        
        service_order_qs = ServicingOrder.objects.filter(invoice_no = invoice_no).last()
        
        if not service_order_qs:
            return ResponseWrapper(error_msg='Service Order is Not Found', status=404)
        
        # if service_order_item_list:
        #     for order_item in service_order_item_list:
        #         order_item_id = order_item.get('item_id')
                
                
        #         created_by = request.user
        #         status_change_reason = f"Order Status Changed By - {created_by.first_name} {created_by.last_name}"
                
        #         if order_item_id:
        #             order_item_qs = OrderItem.objects.filter(id=order_item_id).last()
        #             if not order_item_qs:
        #                 return ResponseWrapper(error_msg='Order Item is Not Found', status=404)

        #             # product_slug = order_item.get('product_slug', order_item_qs.product.slug)
        #             order_item_status = order_item.get('status', order_item_qs.status)
        #             # quantity = order_item.get('quantity', order_item_qs.quantity)
        #             # selling_price = order_item.get('selling_price', order_item_qs.selling_price)
        #             # gsheba_amount = order_item.get('gsheba_amount', order_item_qs.gsheba_amount)
        #             # barcode_number = order_item.get('barcode_number', order_item_qs.barcode_number)
        #         else:
        #             # product_slug = order_item.get('product_slug')
        #             # quantity = order_item.get('quantity')
        #             # selling_price = order_item.get('selling_price')
        #             # gsheba_amount = order_item.get('gsheba_amount')
        #             # barcode_number = order_item.get('barcode_number')
                    
        #             order_item_status = order_item.get('status')
                    
        #         # if order_item_status in  ['CANCELLED'] and not order_status_reason:
        #         #     return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' Status Change Reason is Mandatory when the Status is '{status}' ", status=404)
                
        #         order_item_qs = service_order_create_or_update(invoice_no= invoice_no,servicing_type = 'ORDER', order = order_qs, request_user = request.user, status = 'WAREHOUSE_TO_SERVICE_POINT', order_date = today)
                
        #         is_valid = order_item_qs.get('is_valid')
        #         error_msg = order_item_qs.get('error_msg')
                
        #         if not is_valid:
        #             return ResponseWrapper(error_msg=error_msg, status=404) 
                
        
        profile_image_url = None
            
        user_information_qs =  UserInformation.objects.filter(user = request.user).last()
        if user_information_qs:
            profile_image_url = user_information_qs.image
            
            status_change_by = BaseSerializer(request.user).data
            
        if status:
            # order_status_log_qs = OrderStatusLog.objects.filter(order__invoice_no = order_qs.invoice_no)
            
            # if order_status_log_qs:
            #     return_order_log_qs = order_status_log_qs.filter(status='RETURNED')
                
            #     if not return_order_log_qs:
            #         order_status_log_qs = order_status_log_qs.filter(status='RETURNED').filter(status = status).last()
                
            #         if order_status_log_qs:
            #             return ResponseWrapper(error_msg=f"#{invoice_no} Order Status is Already in '{order_status_log_qs.status_display}'", status=400)
                
            # if status in  ['CANCELLED'] and not order_status_reason:
            #     return ResponseWrapper(error_msg=f"For Order = '{invoice_no}' Status Change Reason is Mandatory when the Status is '{status}' ", status=404)
            
            service_order_qs.status = status
            service_order_qs.save()
            
            if service_order_item_list:
                order_item_qs = service_order_qs.service_order_items.filter(status = status)
                order_item_qs.update(status = status)
            
            serializer = ServiceOrderDetailsSerializer(instance=service_order_qs)
            
            order_info_data = serializer.data
        
            status_display = order_info_data['status_display']
            
            today = TODAY 
            
            #TODO Order Status Update

            # generate_service_order_status_log(
            #     order_obj= service_order_qs,
            #     status= status,
            #     status_display= status_display,
            #     order_status_reason = order_status_reason,
            #     status_change_by = status_change_by,
            #     order_status_change_at = today,
            #     created_by = request.user
            #     )
            
        serializer = ServiceOrderDetailsSerializer(instance=service_order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    

def stream_data(serializer):
    headers = [
        'Invoice No', 'Order Date', 'Status', 'Customer Name', 'Customer Phone',
        'Customer Email', 'Customer Address',
    ]
    yield ','.join(headers) + '\n'
    start_time = time.time()
    for order in serializer.data:
        yield ','.join(str(order[field]) for field in headers) + '\n'
        if time.time() - start_time > 10:
            break
        
class OrderDownloadViewSet(CustomViewSet):
    queryset = OrderItem.objects.all().order_by("-order__order_date")
    lookup_field = 'invoice_no'
    serializer_class = OrderListDownloadSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = OrderItemReportFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    # @staticmethod
    # async def generate_excel(serializer_data):
    #     df = pd.DataFrame(serializer_data)
    #     stream = io.BytesIO()
    #     df.to_excel(stream, index=False)
    #     stream.seek(0)
    #     return stream.getvalue()

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):

            
    # TODO
    
    @log_activity
    def list(self, request, *args, **kwargs):
        import pytz
        # Extract parameters from request
         # Extract parameters from request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        store_name = request.GET.get('office_location')
        payment_status = request.GET.get('payment_status')
        order_type = request.GET.get('order_type')
        status = request.GET.get('status')
        search = request.GET.get('search')
        
        # Construct SQL query with dynamic filtering
        query = """
        SELECT
            ROW_NUMBER() OVER (ORDER BY o.order_date) AS "SI",
            DATE(o.order_date AT TIME ZONE 'UTC') AS "Order Date",
            o.invoice_no AS "Voucher Number",
            ca.name AS "Customer Name",
            ca.phone AS "Mobile",
            ca.email AS "Email",
            ca.address AS "Address",
            cs.name AS "Courier Name",
            s.name AS "Store Name",
            INITCAP(REPLACE(LOWER(o.status), '_', ' ')) AS "Order Status",
            INITCAP(REPLACE(LOWER(o.order_type), '_', ' ')) AS "Order Type",
            INITCAP(REPLACE(LOWER(o.payment_type), '_', ' ')) AS "Payment Type",
            o.remarks AS "Note",
            INITCAP(REPLACE(LOWER(o.payment_status), '_', ' ')) AS "Payment Status",
            dm.delivery_type AS "Delivery Type",
            INITCAP(REPLACE(LOWER(dm.delivery_type), '_', ' ')) AS "Delivery Method",
            oi.barcode_number AS "Barcode",
            oi.promo_code AS "Promo Code",
            p.name AS "Product Name",
            
            -- Aggregated Category Names
            COALESCE(pc.categories, 'N/A') AS "Category Names",
            
            -- Aggregated Subcategory Names
            COALESCE(psc.subcategories, 'N/A') AS "Subcategory Names",
            
            sl.name AS "Seller",
            b.name AS "Brand",
            oi.unit_msp_price AS "MSP",
            oi.unit_mrp_price AS "MRP",
            p.product_code AS "Product Code",
            oi.quantity AS "Quantity",
            oi.selling_price AS "Selling Price",
            oi.total_product_price AS "Total Product Price Per Item",
            oi.total_discount_amount AS "Total Discount Amount Per Item",
            oi.total_net_price AS "Total Net Price Per Item",
            oi.gsheba_amount AS "Total GSheba Amount",
            o.total_delivery_charge AS "Total Delivery Charge",
            oi.total_tax_amount AS "Total Tax Amount Per Item",
            o.total_promo_discount AS "Total Promo Discount",
            o.total_advance_amount AS "Total Advance Amount",
            o.total_due_amount AS "Total Due Amount",
            o.total_payable_amount AS "Total Payable Amount",
            ei.employee_id AS "Order By Employee ID",
            ei.name AS "Order By Employee Name"
        FROM
            order_order o
        LEFT JOIN
            order_customeraddressinfolog ca ON o.id = ca.order_id
        LEFT JOIN
            order_orderitem oi ON o.id = oi.order_id
        LEFT JOIN
            order_deliverymethod dm ON o.delivery_method_id = dm.id
        LEFT JOIN
            location_officelocation s ON o.shop_id = s.id
        LEFT JOIN
            product_management_product p ON oi.product_id = p.id
        LEFT JOIN
            product_management_brand b ON p.brand_id = b.id
        LEFT JOIN
            courier_management_courier c ON o.id = c.order_id
        LEFT JOIN
            courier_management_courierservice cs ON c.courier_service_id = cs.id
        LEFT JOIN
            product_management_seller sl ON p.brand_id = sl.id
        LEFT JOIN 
            human_resource_management_employeeinformation ei ON oi.created_by_id = ei.user_id
        -- Subquery to aggregate category names
        LEFT JOIN (
            SELECT
                pc.product_id,
                STRING_AGG(c.name, ', ') AS categories
            FROM
                public.product_management_product_category pc
            JOIN
                public.product_management_category c ON pc.category_id = c.id
            GROUP BY
                pc.product_id
        ) pc ON p.id = pc.product_id
        -- Subquery to aggregate subcategory names
        LEFT JOIN (
            SELECT
                psc.product_id,
                STRING_AGG(c.name, ', ') AS subcategories
            FROM
                public.product_management_product_sub_category psc
            JOIN
                public.product_management_category c ON psc.category_id = c.id
            GROUP BY
                psc.product_id
        ) psc ON p.id = psc.product_id
        WHERE 1=1
            AND p.name IS NOT NULL
        """

        params = []

        # Apply filters based on parameters
        if start_date and end_date:
            query += " AND DATE(o.order_date) BETWEEN %s AND %s"
            params.append(start_date)
            params.append(end_date)
        
        if store_name:
            query += " AND s.slug = %s"
            params.append(store_name)
        
        if payment_status:
            query += " AND o.payment_status = %s"
            params.append(payment_status)

        if status:
            query += " AND o.status = %s"
            params.append(status)

        if order_type:
            query += " AND o.order_type = %s"
            params.append(order_type)
        
        if search:
            query += """
                AND (
                    o.invoice_no ILIKE %s OR
                    ca.name ILIKE %s OR
                    ca.email ILIKE %s
                )
            """
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])

        query += """
            ORDER BY
                o.order_date;
            """

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        # Check if there is any data to serialize
        if not rows:
            return HttpResponse("No data found")

        # Define the headers
        headers = [
            'SI', 'Order Date', 'Voucher Number', 'Customer Name', 'Mobile', 'Email', 'Address', 
            'Courier Name', 'Store Name', 'Order Status', 'Order Type', 'Payment Type', 'Note', 
            'Payment Status', 'Delivery Type', 'Delivery Method', 'Barcode', 'Promo Code', 'Product Name','Category Names','Subcategory Names', 'Seller', 'Brand', 
            'MSP', 'MRP', 'Product Code', 'Quantity', 'Selling Price', 'Total Product Price', 
            'Total Discount Amount', 'Total Net Payable Amount', 'Total GSheba Amount', 'Total Delivery Charge', 
            'Total Tax Amount', 'Total Promo Discount', 'Total Advance Amount', 'Total Due Amount', 
            'Total Payable Amount', 'Order Creator Employee ID', 'Employee Name'
        ]

        # Create an XLSX file
        wb = Workbook()
        ws = wb.active

        # Write headers to the first row
        ws.append(headers)

        # Write data rows
        for row in rows:
            # Convert timezone-aware datetimes to naive datetimes
            row_data = []
            for value in row:
                if isinstance(value, datetime):
                    # Convert timezone-aware datetime to naive datetime
                    if value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                row_data.append(value)
            ws.append(row_data)

        # Get today's date
        today_date = datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d')

        # Create a file-like response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=orders_{today_date}.xlsx'

        # Save workbook to response
        wb.save(response)

        return response
