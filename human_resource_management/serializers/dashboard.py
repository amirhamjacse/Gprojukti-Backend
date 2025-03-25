from datetime import datetime
from rest_framework import serializers
from base.models import PaymentType
from base.serializers import EmployeeInformationBaseSerializer, UserInformationBaseSerializer
from gporjukti_backend_v2 import settings
from human_resource_management.models.attendance import *
from human_resource_management.models.calender import EventOrNotice
from human_resource_management.serializers.employee import EmployeeInformationListSerializer
from order.models import Order, OrderItem
from product_management.models.product import Product
from utils.base import product_image
from django.db.models import Sum

import random

class DashboardNoticeListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EventOrNotice
        fields = [
                   'id',
                   'name',
                   'slug',
                   'description',
                   'start_date',
                   'end_date',
                   'color'
                ]
        
class ShopWiseSellSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField(read_only = True)
    total_sell_amount = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Order
        fields = [
                   'quantity',
                   'total_sell_amount',
                ]
        
    def get_quantity(self, obj):
        quantity = 5
        return quantity
    
        

class DashboardTopProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)
    brand = serializers.SerializerMethodField(read_only=True)
    supplier = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'total_quantity',
            'brand',
            'supplier',
        ]
        
    def get_total_quantity(self, obj):
        return obj.total_quantity
    
    def get_image(self, obj):
        return product_image(product=obj)
    
    def get_brand(self, obj):
        return obj.brand.name if obj.brand else '-'
    
    def get_supplier(self, obj):
        return obj.supplier.name if obj.supplier else '-'
    
class DashboardSellOverviewListSerializer(serializers.ModelSerializer):
    msg = serializers.SerializerMethodField(read_only = True)
    quantity = serializers.SerializerMethodField(read_only = True)
    total_amount = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Order
        fields = [
                   'msg',
                   'quantity',
                   'total_amount'
                ]
        
        def get_msg(self, obj):
            msg = 'Total '
            return msg
        
        
        def get_quantity(self, obj):
            quantity = random.randint(1, 100)
            return quantity
        
        
        def get_total_amount(self, obj):
            total_amount = random.randint(8888, 99999)
            return total_amount
            
# class DashboardSellListSerializer(serializers.ModelSerializer):
    weekly_day_wise_order_quantity = serializers.SerializerMethodField(read_only = True)
    weekly_day_wise_total_order_amount = serializers.SerializerMethodField(read_only = True)
    weekly_day_wise_order_date_list = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Order
        fields = [
                   'weekly_day_wise_order_quantity',
                   'weekly_day_wise_total_order_amount',
                   'weekly_day_wise_order_date_list'
                ]
        
    def get_weekly_day_wise_order_quantity(self, obj):
        # Assuming `obj` is a queryset of orders for a week
        today = settings.TODAY.date()
        weekly_day_wise_order_quantity = []

        for i in range(7):
            day = today - timedelta(days=i)
            count = obj.filter(order_date=day).count()
            weekly_day_wise_order_quantity.append(count)

        return weekly_day_wise_order_quantity

    def get_weekly_day_wise_total_order_amount(self, obj):
        # Assuming `obj` is a queryset of orders for a week
        today = settings.TODAY.date()
        weekly_day_wise_total_order_amount = []

        for i in range(7):
            day = today - timedelta(days=i)
            total_amount = obj.filter(order_date=day).aggregate(total_amount=Sum('total_payable_amount'))['total_amount'] or 0
            
            weekly_day_wise_total_order_amount.append(total_amount)

        return weekly_day_wise_total_order_amount

    def get_weekly_day_wise_order_date_list(self, obj):
        today = settings.TODAY.date()
        weekly_day_wise_order_date_list = sorted([str(today - timedelta(days=i)) for i in range(7)], reverse=True)
        return weekly_day_wise_order_date_list
    
    
class DashboardSellWiseEmployeeListSerializer(serializers.ModelSerializer):
    sell_details = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = EmployeeInformation
        fields = [
                   'employee_id',
                   'name',
                   'slug',
                   'image',
                   'sell_details',
                ]
        
    def get_sell_details(self, obj):
        total_order = random.randint(1, 100)
        total_received_order = random.randint(1, 100)
        total_delivered_order = random.randint(1, 100)
        total_cancel_order = random.randint(1, 100)
        
        sell_details = {
            'total_order':total_order,
            'total_received_order':total_received_order,
            'total_delivered_order':total_delivered_order,
            'total_cancel_order':total_cancel_order,
        }
        return sell_details    
    
class DashboardPaymentAmountListSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = PaymentType
        fields = [
                   'id',
                   'name',
                   'slug',
                   'logo',
                   'total_amount',
                ]
        
    def get_total_amount(self, obj):
        total_amount = random.randint(8736, 999999)
        
        return total_amount
    
class DashboardEmployeeAttendanceListSerializer(serializers.ModelSerializer):
    # employee_information = EmployeeInformationListSerializer(read_only = True)
    employee_information = serializers.SerializerMethodField(read_only = True)
    check_in = serializers.SerializerMethodField(read_only = True)
    attendance_type_display = serializers.CharField(source='get_attendance_type_display')
    class Meta:
        model = EmployeeAttendance
        fields = [
                   'id',
                   'employee_information',
                   'check_in',
                   'attendance_type',
                   'attendance_type_display',
                ]
        
    def get_employee_information(self, obj):
        if obj.employee_information:
            employee_qs = EmployeeInformation.objects.all().filter(slug =  obj.employee_information.slug).order_by("?").last()
        else:
            employee_qs = EmployeeInformation.objects.all().order_by("?").last()
            
        name = employee_qs.name
        employee_id = employee_qs.employee_id
        image = employee_qs.image
        
        context = {
            'name':name,
            'employee_id':employee_id,
            'image':image,
        }
        
        return context
        
    def get_check_in(self, obj):
        check_in = (obj.created_at + timedelta(hours=6)).strftime("%d %B, %Y at %I:%M %p")
        
        return check_in
    
class DashboardEmployeeListSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.SerializerMethodField(read_only = True)
    image = serializers.SerializerMethodField(read_only = True)
    employee_id = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = EmployeeInformation
        fields = [
                   'id',
                   'name',
                   'employee_id',
                   'slug',
                   'image',
                   'date_of_birth',
                   'next_confirmation_date',
                   'joining_date',
                ]
        
    def get_date_of_birth(self, obj): 
        date_of_birth = '10 July' 
        if obj.date_of_birth:
            date_of_birth = obj.date_of_birth.strftime('%d %B')
        
        return date_of_birth
    
    def get_image(self, obj): 
        image = settings.NOT_FOUND_IMAGE 
        
        if obj.image:
            image = obj.image
        
        return image
    
    def get_employee_id(self, obj): 
        employee_id = f"11{obj.id}" 
        
        # if obj.image:
        #     image = obj.image
        
        return employee_id
        
    
        
        
class ShopWisePaymentCollectionListSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = PaymentType
        fields = [
                   'id',
                   'name',
                   'slug',
                   'logo',
                   'total_amount',
                ]
        
    def get_total_amount(self, obj):
        
        total_amount = random.randint(8736, 999999)
        
        return total_amount
