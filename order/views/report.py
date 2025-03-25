from gporjukti_backend_v2.settings import BASE_URL, TODAY
from human_resource_management.filters import EmployeeInformationFilter
from human_resource_management.serializers.dashboard import DashboardPaymentAmountListSerializer, DashboardTopProductListSerializer
from human_resource_management.serializers.employee import EmployeeInformationListSerializer
from order.models import *
from order.serializers import *
from human_resource_management.models.employee import EmployeeInformation
from product_management.models.product import ProductStock, Product
from product_management.serializers.product import ProductStockListSerializer
from product_management.utils import barcode_status_log
from user.models import UserType
from utils.actions import activity_log
from utils.decorators import log_activity
from utils.calculate import generate_service_order_status_log, service_order_create_or_update, generate_order_status_log, offer_check, order_item_create, order_payment_log
from utils.custom_veinlet import CustomViewSet
from utils.generates import generate_invoice_no, generate_service_invoice_no, unique_slug_generator
from utils.permissions import CheckCustomPermission
from utils.response_wrapper import ResponseWrapper
from utils.upload_image import image_upload
from django.utils import timezone
from order.filters import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from utils.base import get_user_store_list, render_to_pdf
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated

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
from django.db.models import Sum

from base.models import ORDER_STATUS, ORDER_TYPE


    
class AdminOrderReportViewSet(CustomViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    lookup_field = 'pk'
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = OrderFilter
    
    def get_queryset(self):
        if self.action == 'payment_type_wise_collection_list':
            return OrderPaymentLog.objects.all().order_by('id')
        elif self.action == 'top_sell_product_list':
            return Product.objects.all().order_by('id')
        elif self.action == 'product_stock_report_list':
            return ProductStock.objects.all().order_by('id')
        else:
            return Order.objects.all().order_by('-order_date')
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = OrderCreateSerializer
        else:
            self.serializer_class = OrderListSerializer

        return self.serializer_class
    
    def get_filterset_class(self):
        if self.action in ['payment_type_wise_collection_list']:
            self.filterset_class = OrderPaymentLogReportFilter
        elif self.action in ['top_sell_product_list']:
            self.filterset_class = TopProductSellReportFilter
        elif self.action in ['product_stock_report_list']:
            self.filterset_class = ProductStockReportFilter
        else:
            self.filterset_class = OrderFilter

        return self.filterset_class
    
    def order_overview(self, queryset, order_type, msg):
        quantity = 0
        ratio = 0
        
        qs = queryset.filter(order_type=order_type)
        quantity = qs.count()
        ratio = round((quantity / queryset.count()) * 100, 2)
        
        context = {
            'msg': msg,
            'quantity': quantity,
            'ratio': f"{str(ratio)}%",
        }
        
        return context

    @log_activity
    def order_report_overview_list(self, request, *args, **kwargs):
        order_qs = Order.objects.filter()
        
        ecommerce_order = self.order_overview(queryset=order_qs, order_type='ECOMMERCE_SELL', msg='Total Ecommerce Order')
        e_retail_order = self.order_overview(queryset=order_qs, order_type='RETAIL_ECOMMERCE_SELL', msg='Total E-Retail Order')
        point_of_sell_order = self.order_overview(queryset=order_qs, order_type='POINT_OF_SELL', msg='Total Point Of Sell')
        on_the_go_order = self.order_overview(queryset=order_qs, order_type='ON_THE_GO', msg='Total On The Go Order')
        corporate_order = self.order_overview(queryset=order_qs, order_type='CORPORATE_SELL', msg='Total Corporate Order')
        b2b_order = self.order_overview(queryset=order_qs, order_type='B2B_SELL', msg='Total B2B Order')
        gift_order = self.order_overview(queryset=order_qs, order_type='GIFT_ORDER', msg='Total Gift Order')
        pc_builder_order = self.order_overview(queryset=order_qs, order_type='PC_BUILDER_SELL', msg='Total PC Builder Order')
        pre_order = self.order_overview(queryset=order_qs, order_type='PRE_ORDER', msg='Total Pre Order')
        replacement_order = self.order_overview(queryset=order_qs, order_type='REPLACEMENT_ORDER', msg='Total Replacement Order')
        
        quantity = order_qs.count()
        ratio = round((quantity / order_qs.count()) * 100, 2)
        
        all_order = {
            'msg': 'All Order',
            'quantity': quantity,
            'ratio': f"{str(ratio)}%",
        }
        
        context = [
            all_order,
            ecommerce_order,
            e_retail_order,
            point_of_sell_order,
            on_the_go_order,
            corporate_order,
            b2b_order,
            gift_order,
            pc_builder_order,
            pre_order,
            replacement_order
        ]
        
        return ResponseWrapper(data=context, msg="Success", status=200)
    
    def order_status_overview(self, queryset, status, msg):
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

    @log_activity
    def order_report_status_overview_list(self, request, *args, **kwargs):
        order_qs = Order.objects.filter()
        
        order_list = []
        all_order_status_list = ORDER_STATUS
        
        for status_tuple in all_order_status_list:
            full_status, status_display = status_tuple 
            
            order_details = self.order_status_overview(queryset=order_qs, status=full_status, msg=f'Total {status_display}')
            
            order_list.append(order_details) 
        
        return ResponseWrapper(data=order_list, msg="Success", status=200)
        

    @log_activity
    def top_sell_product_list(self, request, *args, **kwargs):
        order_item_qs = OrderItem.objects.filter().exclude(status__in=['CANCELLED', 'RETURNED'])
        
        qs = Product.objects.filter(slug__in=order_item_qs.values_list('product__slug', flat=True)).annotate(
            total_quantity=Sum('order_items__quantity')
        ).order_by('-total_quantity')
        
        filterset_class = self.get_filterset_class()
        filtered_qs = filterset_class(request.GET, queryset=qs).qs

        page_qs = self.paginate_queryset(filtered_qs.order_by('-total_quantity'))
        serializer = DashboardTopProductListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

    @log_activity
    def payment_type_wise_collection_list(self, request, *args, **kwargs):
        qs = OrderPaymentLog.objects.all().order_by('id')
        
        # Apply filters using the correct filterset class
        filterset_class = self.get_filterset_class()
        filtered_qs = filterset_class(request.GET, queryset=qs).qs
        
        # Paginate the filtered queryset
        page_qs = self.paginate_queryset(filtered_qs)
        serializer = OrderPaymentLogReportSerializer(instance=page_qs, many=True)

        # Return paginated response
        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

        
    @log_activity
    def product_stock_report_list(self, request, *args, **kwargs):
        store_qs = OfficeLocation.objects.all()
        # store_qs = get_user_store_list(request_user = request.user)
        
        # qs = ProductStock.objects.filter(stock_location__slug__in = store_qs.values_list('slug', flat=True)).exclude(stock_location = None)
        qs = ProductStock.objects.filter(stock_location__slug__in = store_qs.values_list('slug', flat=True))
        
        filterset_class = self.get_filterset_class()
        filtered_qs = filterset_class(request.GET, queryset=qs).qs

        page_qs = self.paginate_queryset(filtered_qs)
        
        serializer = ProductStockListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)