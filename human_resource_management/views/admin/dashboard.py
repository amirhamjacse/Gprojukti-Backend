from django.conf import settings
from base.models import PaymentType
from gporjukti_backend_v2.settings import TODAY
from human_resource_management.filters import *
from human_resource_management.models.calender import EventOrNotice
from human_resource_management.serializers.dashboard import *
from order.filters import OrderReportFilter
from order.models import Order
from product_management.models.product import *
from django.http import HttpResponse
from utils.base import get_user_store_list
from utils.decorators import log_activity
from utils.response_wrapper import ResponseWrapper

from django.db.models import Q

# User = get_user_model()
from utils.permissions import CheckCustomPermission
# import re
from human_resource_management.serializers.employee import *
from human_resource_management.models.employee import *
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from utils.permissions import *
from django.db import transaction
# Create your views here.
from rest_framework.generics import get_object_or_404  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from drf_extra_fields.fields import Base64FileField, Base64ImageField

import asyncio

import random
from datetime import datetime, timedelta

 
class DashboardViewSet(CustomViewSet):
    queryset = EmployeeDivision.objects.all()
    lookup_field = 'pk'
    serializer_class = EmployeeDivisionSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = EmployeeDivisionFilter
    

    def get_queryset(self):
        if self.action == 'shop_wise_sell_list':
            return Order.objects.all()
        return super().get_queryset()
    

    def get_filterset_class(self):
        if self.action == 'shop_wise_sell_list':
            return OrderReportFilter
        return EmployeeDivisionFilter
    

    def get_filterset(self, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        if not filterset_class:
            return None
        return filterset_class(*args, **kwargs)
    
    def get_permissions(self):
        if self.action in ["shop_wise_pos_dashboard"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    @log_activity
    def shop_wise_pos_dashboard(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request_user = request.user).filter(office_type__in= ['STORE', 'WAREHOUSE', 'BRANCH']).last()
        
        today = timezone.now().date()
         
        if not shop_qs:
            return ResponseWrapper(error_msg='Shop Information is Not Found', error_code= 404)
        
        total_pos_order_qty = 0.0
        total_pos_order_amount = 0.0
        total_e_retail_order_qty = 0.0
        total_e_retail_order_amount = 0.0
        total_shop_to_home_delivery_order_qty = 0
        total_shop_to_home_delivery_order_amount = 0.0
        
        total_inventory = 0.0
        total_active_inventory = 0.0
        total_faulty_inventory = 0.0
        total_gsheba_faulty_inventory = 0.0
        total_others_inventory = 0.0 
        
        product_stock_qs = ProductStock.objects.filter(stock_location = shop_qs, status__in = ["ACTIVE"]).exclude(status='SOLD')
        
        total_inventory = product_stock_qs.count()
 
        total_active_inventory = product_stock_qs.filter(status='ACTIVE').count()
 
        total_gsheba_faulty_inventory = product_stock_qs.filter(status='GSHEBA_FAUlLY').count() 

        # Calculate total_others_inventory 
        total_others_inventory = total_inventory - (total_active_inventory + total_gsheba_faulty_inventory)
        
        # order_qs = Order.objects.filter(shop__slug = shop_qs.slug)
        
        print(f'Today = {timezone.now()}, {today}, Shop Name = {shop_qs.name}')
        
        order_qs = Order.objects.filter(order_date__date = today, shop = shop_qs, status = "DELIVERED")
        
        total_pos_order_qty = order_qs.filter(order_type = 'POINT_OF_SELL').count()
        # print(f'Invoice List = {order_qs.filter(order_type = 'POINT_OF_SELL').values_list('invoice_no', flat=True)}')
        
        total_pos_order_amount = sum(order_qs.filter(order_type = 'POINT_OF_SELL', status = 'DELIVERED').values_list('total_payable_amount', flat = True))
        
        total_e_retail_order_qty = order_qs.filter(order_type = 'RETAIL_ECOMMERCE_SELL').count()
        total_e_retail_order_amount = sum(order_qs.filter(order_type = 'RETAIL_ECOMMERCE_SELL').values_list('total_payable_amount', flat = True))
        
        
        context = {
            'total_pos_order_qty': total_pos_order_qty, 
            'total_pos_order_amount': total_pos_order_amount, 
            'total_e_retail_order_qty': total_e_retail_order_qty, 
            'total_e_retail_order_amount': abs(total_e_retail_order_amount), 
            'total_inventory': total_inventory, 
            'total_active_inventory': total_active_inventory, 
            # 'total_faulty_inventory': total_faulty_inventory, 
            'total_gsheba_faulty_inventory': total_gsheba_faulty_inventory, 
            'total_others_inventory': total_others_inventory,
            'today': today,
            
        }
        
        return ResponseWrapper(data=context, msg="Success", status= 200)
    
    @log_activity
    def shop_wise_notice(self, request, *args, **kwargs):
        shop_slug= 'gg'
        shop_qs = OfficeLocation.objects.filter(slug=  shop_slug, office_type= 'STORE').last()
        # if not shop_qs:
        #     return ResponseWrapper(error_msg='Shop Information is Not Found', error_code= 404)
    
        notice_qs = EventOrNotice.objects.filter(
            # type = 'NOTICE', office_location__slug = shop_slug
        ).order_by('-id')[:5]
        serializer = DashboardNoticeListSerializer(instance=notice_qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def shop_wise_employee_performance(self, request, *args, **kwargs):
        shop_slug= get_user_store_list(request.user).last()
        
        
        shop_qs = OfficeLocation.objects.filter(slug=  shop_slug.slug).last()
        
        today = timezone.now()
        
        employee_list = []
        
        employee_list_qs = EmployeeInformation.objects.filter(
            work_station__slug = shop_qs.slug, user__user_informations__user_type__name = "Employee"
        ).order_by('employee_id')[:3]
        
        for employee in employee_list_qs:
            employee_image = settings.NOT_FOUND_IMAGE
            
            id = employee.id
            name = employee.name
            employee_slug = employee.slug
            
            if employee.image:
                employee_image = employee.image
              
            order_item_qs = OrderItem.objects.filter(
                created_by__email = employee.user.email,
                order__order_date__month = today.month
            ) 
            
            order_qs = Order.objects.filter(
                order_items__created_by__email = employee.user.email,
                order_date__month = today.month
            )  
            
            total_sell_quantity = order_item_qs.count()
            
            total_sell_amount = sum(order_item_qs.values_list('selling_price', flat = True))
            
            total_commission_amount = sum(order_item_qs.values_list('commission_amount', flat = True))
            
            context = {
                'id': id,
                'name': name,
                'employee_slug': employee_slug,
                'employee_image': employee_image,
                'total_sell_quantity': total_sell_quantity,
                'total_sell_amount': total_sell_amount,
                'total_commission_amount': 0.0,
            }
        
            employee_list.append(context)

        
        context = employee_list
        
        return ResponseWrapper(data=context, msg="Success", status= 200)
    

    @log_activity
    def shop_wise_sell_list(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request.user)
        shop_slug_list = shop_qs.values_list('slug', flat=True)
        
        qs = Order.objects.filter(
            Q(shop__slug__in = shop_slug_list)
            | Q(pickup_shop__slug__in = shop_slug_list)
            | Q(return_shop__slug__in = shop_slug_list)
        )
        
        print('qs', qs.last().order_type)
        
        filterset_class = self.get_filterset_class()
        filtered_qs = filterset_class(request.GET, queryset=qs).qs
        
        today = timezone.now().date()
        
        weekly_day_wise_order_quantity = []
        weekly_day_wise_total_order_amount = []
        weekly_day_wise_order_date_list = []
        
        is_online =  request.GET.get('is_online')
        is_offline =  request.GET.get('is_offline')
        
        # if is_online == True
        
        for i in range(7):
            day = today - timedelta(days=i)
            print(f"day = {day}")
            
            order_qs = filtered_qs.filter(order_date__date = day)
            
            total_order = order_qs.count()
            total_order_amount = sum(order_qs.values_list('total_payable_amount', flat = True))
            
            weekly_day_wise_order_quantity.append(total_order)
            weekly_day_wise_total_order_amount.append(abs(total_order_amount))
            weekly_day_wise_order_date_list.append(day)
            

        context = {
            'weekly_day_wise_order_quantity': weekly_day_wise_order_quantity,
            'weekly_day_wise_total_order_amount': weekly_day_wise_total_order_amount,
            'weekly_day_wise_order_date_list': weekly_day_wise_order_date_list,
        }
        
        return ResponseWrapper(data=context, msg="Success", status=200)
    
    
    @log_activity
    def online_sell_overview_list(self, request, *args, **kwargs):
        qs = Order.objects.all()
        today = timezone.now()
        week = 7
        
        # serializer = DashboardSellOverviewListSerializer(qs)
        
        context = [
                    {
                        'msg': 'Total Received Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                    {
                        'msg': 'Total Advance Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                    {
                        'msg': 'Total Ecommerce Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                    {
                        'msg': 'Total E-Retail Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                    {
                        'msg': 'Total Dispatch Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                    {
                        'msg': 'Total Cancelled Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                    {
                        'msg': 'Total Return Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,99999),
                    },
                    {
                        'msg': 'Total G-Sheba Order',
                        'total_order_qty': random.randint(1, 100),
                        'total_order_amount': random.randint(7777,9999),
                    },
                   ]
        
        return ResponseWrapper(data=context, msg="Success", status= 200)
    
    @log_activity
    def online_active_notice_list(self, request, *args, **kwargs):
        notice_qs = EventOrNotice.objects.filter(
            # type = 'NOTICE', office_location__slug = shop_slug
        )[:5]
        serializer = DashboardNoticeListSerializer(instance=notice_qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def upcoming_holiday_list(self, request, *args, **kwargs):
        notice_qs = EventOrNotice.objects.filter().order_by('id')[:2]
        
        serializer = DashboardNoticeListSerializer(instance=notice_qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def online_top_sell_product_list(self, request, *args, **kwargs):
        qs = Product.objects.filter(
            # type = 'NOTICE', office_location__slug = shop_slug
        ).order_by('?')[:5]
        serializer = DashboardTopProductListSerializer(instance=qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def dashboard_sell_report(self, request, *args, **kwargs):
        qs = Order.objects.filter(
            
        )
        serializer = DashboardSellListSerializer(instance=qs)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def dashboard_employee_sales_report(self, request, *args, **kwargs):
        qs = EmployeeInformation.objects.filter(
            
        ).order_by('?')[:5]
        serializer = DashboardSellWiseEmployeeListSerializer(instance=qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    

    @log_activity
    def payment_type_wise_received_amount_list(self, request, *args, **kwargs):
        qs = PaymentType.objects.filter().order_by('id')
        
            
        serializer = DashboardPaymentAmountListSerializer(instance=qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    
    @log_activity
    def dashboard_hrm_employee_attendance(self, request, *args, **kwargs):
        today = timezone.now()
        qs = EmployeeAttendance.objects.filter(check_in__date = today.date()).exclude(employee_information__user__user_informations__user_type__name__icontains = "Shop User").order_by('check_in')[:5]
        
            
        serializer = DashboardEmployeeAttendanceListSerializer(instance=qs, many = True)
        
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def dashboard_hrm_employee_notice(self, request, *args, **kwargs):
        qs = EventOrNotice.objects.filter().order_by('-created_at')[:5]
            
        serializer = DashboardNoticeListSerializer(instance=qs, many = True)

        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def dashboard_hrm_employee_birthday(self, request, *args, **kwargs):
        qs = EmployeeInformation.objects.filter(work_station__office_type = "HEAD_OFFICE", user__is_superuser = True).order_by('?')[:5]
            
        serializer = DashboardEmployeeListSerializer(instance=qs, many = True)
        
                
        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)
    
    @log_activity
    def dashboard_hrm_upcoming_joining_employee(self, request, *args, **kwargs):
        qs = EmployeeInformation.objects.filter()[:5]
            
        serializer = DashboardEmployeeListSerializer(instance=qs, many = True)

        return ResponseWrapper(data=serializer.data, msg="Success", status= 200)


class EmployeeAttendanceViewSet(CustomViewSet):
    queryset = EmployeeAttendance.objects.all()
    lookup_field = 'pk'
    serializer_class = EmployeeDivisionSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = EmployeeAttendenceFilter

    @staticmethod
    async def generate_excel(serializer_data):
        import io
        import pandas as pd
        df = pd.DataFrame(serializer_data)
        stream = io.BytesIO()
        df.to_excel(stream, index=False)
        stream.seek(0)
        return stream.getvalue()


    def list(self, request, *args, **kwargs):
        from asgiref.sync import async_to_sync
        import pytz
        from datetime import datetime
        from django.db import connection
        import pandas as pd

        search_name = request.GET.get('search')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        employee_id = request.GET.get('employee_id')
        check_in_str = request.GET.get('check_in')
        check_out_str = request.GET.get('check_out')
        attendance_type = request.GET.get('attendance_type')

        # Base SQL query
        query = """
            SELECT 
                ROW_NUMBER() OVER () AS "SI",
                ei.employee_id AS "Employee ID",
                u1.first_name AS "First Name",
                u1.last_name AS "Last Name",
                empl.name AS "Designation",
                INITCAP(REPLACE(LOWER(ea.attendance_type), '_', ' ')) AS "Attendance Type",
                TO_CHAR(ea.working_date AT TIME ZONE 'UTC', 'Mon DD, YYYY') AS "Working Date",
                TO_CHAR(ea.check_in AT TIME ZONE 'UTC', 'Mon DD, YYYY HH12:MI:SS AM') AS "Check In",
                TO_CHAR(ea.check_out AT TIME ZONE 'UTC', 'Mon DD, YYYY HH12:MI:SS AM') AS "Check Out"
                -- ea.remarks AS "Remarks"
            FROM 
                human_resource_management_employeeattendance ea
            LEFT JOIN
                human_resource_management_employeeinformation ei ON ea.employee_information_id = ei.id
            LEFT JOIN
                human_resource_management_employeeofficehour eo ON ea.employee_office_hour_id = eo.id
            LEFT JOIN
                human_resource_management_employeeinformation a ON ea.approved_by_id = a.id
            LEFT JOIN
                human_resource_management_designation empl ON ei.designations_id = empl.id
            LEFT JOIN
                user_useraccount u1 ON ea.created_by_id = u1.id
            LEFT JOIN
                user_useraccount u2 ON ea.updated_by_id = u2.id
            WHERE 1=1
        """

        # Append conditions based on search parameters
        params = []
        if start_date_str and end_date_str:
            query += " AND ea.working_date BETWEEN %s AND %s"
            params.append(start_date_str)
            params.append(end_date_str)
        if search_name:
            query += " AND (u1.first_name ILIKE %s OR u1.last_name ILIKE %s)"
            params.append(f"%{search_name}%")
            params.append(f"%{search_name}%")
        if employee_id:
            query += " AND ei.employee_id = %s"
            params.append(employee_id)
        if check_in_str:
            query += " AND ea.check_in >= %s"
            params.append(check_in_str)
        if check_out_str:
            query += " AND ea.check_out <= %s"
            params.append(check_out_str)
        if attendance_type:
            query += " AND ea.attendance_type = %s"
            params.append(attendance_type)

        # Execute the query and fetch results
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Convert timezone-aware datetimes to naive datetimes
        datetime_columns = [""]
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.tz_localize(None)

        # Generate Excel file asynchronously
        excel_content = async_to_sync(self.generate_excel)(df)

        # Create the HttpResponse object with the appropriate XLSX content-type and headers
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Get today's date in the format you want
        today_date = datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d')

        # Construct the filename with today's date
        filename = f'Employee Attendance - {today_date}.xlsx'

        # Assign the filename to the Content-Disposition header
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response