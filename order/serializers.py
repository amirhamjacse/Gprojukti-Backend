from datetime import timedelta
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer, PaymentTypeSerializer, UserInformationBaseSerializer
from gporjukti_backend_v2 import settings
from gporjukti_backend_v2.settings import TODAY
from location.serializers import OfficeLocationListSerializer
from order.models import *
from django.db.models import Q
from drf_extra_fields.fields import Base64FileField, Base64ImageField


from user.serializers import BaseSerializer
from django.utils import timezone

from utils.calculate import calculate_order_price

import random

import asyncio

from utils.constants import *

class DeliveryMethodListSerializer(serializers.ModelSerializer):
    delivery_type_display = serializers.CharField(source='get_delivery_type_display', read_only =  True)
    
    class Meta:
        model = DeliveryMethod
        fields = [
            'id',
            'delivery_type',
            'delivery_type_display',
            'slug',
            'delivery_charge'
                  ]
        

class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(required=False)
    status_change_reason = serializers.CharField(required=False)
    created_by = serializers.CharField(required=False)
    quantity = serializers.IntegerField(default =1)
    order_item_id = serializers.IntegerField(default =1)
    parent_order_item_id = serializers.IntegerField(default =1)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order_item_id',
            'quantity',
            'status',
            'status_change_reason',
            'product_slug',
            'selling_price',
            'gsheba_amount',
            'barcode_number',
            'parent_order_item_id',
            'created_by',
                  ]
        
class OrderPaymentLogCreateSerializer(serializers.ModelSerializer):
    payment_method_slug = serializers.CharField(required=False)
    
    class Meta:
        model = OrderPaymentLog
        fields = [
            'id',
            'transaction_no',
            'payment_method_slug',
            'received_amount',
                  ]
        
        
class OrderCreateSerializer(serializers.ModelSerializer):
    invoice_no = serializers.CharField(read_only = True)
    shop = serializers.CharField(read_only = True)
    pickup_shop = serializers.CharField(read_only = True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    area_slug = serializers.CharField(required=False)
    address_type = serializers.CharField(required=False)
    employee_id = serializers.CharField(required=False)
    delivery_method_slug = serializers.CharField(required=False)
    order_item_list = OrderItemCreateUpdateSerializer(many= True, write_only = True)
    order_payment_list = OrderPaymentLogCreateSerializer(many= True, write_only = True)
    # order_price_info = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'invoice_no',
            'remarks',
            'shop',
            'pickup_shop',
            'order_date',
            'first_name',
            'last_name',
            'email',
            'phone',
            'area_slug',
            'address',
            'address_type',
            'delivery_method_slug',
            'order_type',
            'payment_type',
            'is_for_employee',
            'payment_status',
            'promo_code',
            'employee_id',
            'total_advance_amount',
            'order_item_list',
            'order_payment_list',
            # 'order_price_info',
                  ]
        
    # def get_order_price_info(self, obj):
    #     price_details = {}
    #     print(f'In Serializer, Invoice No = {obj.invoice_no}')
    #     return price_details
        
class SSLOrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'invoice_no',
            'payment_type',
            'total_advance_amount',
        ]
        
class OrderListSerializer(serializers.ModelSerializer):
    # created_by = BaseSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    status_color = serializers.SerializerMethodField(read_only = True)
    delivery_method = serializers.SerializerMethodField( read_only =  True)
    order_type_display = serializers.CharField(source='get_order_type_display', read_only =  True)
    order_type_color = serializers.SerializerMethodField(read_only = True)
    total_advance_amount = serializers.SerializerMethodField(read_only = True)
    customer_details = serializers.SerializerMethodField(read_only = True)
    shop_name = serializers.SerializerMethodField(read_only = True)
    order_date = serializers.DateTimeField(format="%d %B, %Y, at %I:%M %p")
    
    
    class Meta:
        model = Order
        fields = [
            'id',
            'invoice_no',
            'status',
            'status_display',
            'status_color',
            'order_type_color',
            'delivery_method',
            'order_type',
            'order_type_display',
            'total_advance_amount',
            'total_payable_amount',
            'order_date',
            'customer_details',
            'shop_name',
            # 'created_by',
                  ]
        
    def get_shop_name(self, obj):
        shop_name = "-"
        
        if obj.shop:
            shop_name = obj.shop.name
            
        return shop_name
    
    def get_status_color(self, obj):
        return ORDER_STATUS_COLORS.get(obj.status, "#FF0000")
    
    def get_order_type_color(self, obj):
        return ORDER_TYPE_COLORS.get(obj.order_type, "#FF0000")
    
    def get_total_advance_amount(self, obj):
        return obj.total_paid_amount
    
        
    def get_customer_details(self, obj):
        context = {}
        
        user_type = 'Customer'
        email = '-'
        customer_name = '-'
        image = '-'
        phone = '-'
        
        # print('obj.customer_address_logs.all().last()', obj.customer_address_logs.all().last().name)
        
        image_url = None
        
        if obj.customer:
            image_url = obj.customer.image
        
        if obj.customer_address_logs.last():
            id = obj.customer_address_logs.last().id
            customer_name = obj.customer_address_logs.last().name
            email = obj.customer_address_logs.last().email
            phone = obj.customer_address_logs.last().phone
            
            print('fffffffff', phone)
            
            if '@' in phone:
                phone = '-'
                    
        context = {
            # 'id': obj.customer.user.id,
            'name': customer_name,
            'user_type': user_type,
            'email':  email,
            'phone': phone,
            'image': image_url,
        }

        return context

    
    def get_delivery_method(self, obj):
        context = {}
        
        id  = None
        name  = None
        
        if obj.order_type == 'POINT_OF_SELL':
            name = 'Store Sell'
            
        if obj.delivery_method:
            id = obj.delivery_method.id
            name = obj.delivery_method.get_delivery_type_display()
        
        context = {
            'id': id,
            'name': name,
        }
        
        return context

    
class OrderPaymentLogListSerializer(serializers.ModelSerializer):
    order_payment_details = serializers.SerializerMethodField(read_only = True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    
    class Meta:
        model = OrderPaymentLog
        fields = [
            'slug',
            'transaction_no',
            'status',
            'status_display',
            'order_payment_details',
            'received_amount',
            'remaining_amount',
            'created_at',
                  ]
        
    def get_order_payment_details(self, obj):
        context = {}
        if obj.order_payment:
        
            context  = {
                'id': obj.order_payment.id,
                'name': obj.order_payment.name,
                'slug': obj.order_payment.slug,
                'logo': obj.order_payment.logo
            }
            
        return context
        
            
class OrderItemWarrantyLogSerializer(serializers.ModelSerializer):
    warranty_type_display = serializers.CharField(source='get_warranty_type_display', read_only =  True)
    warranty_duration_display = serializers.CharField(source='get_warranty_duration_display', read_only =  True)
    remaining_days = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = OrderItemWarrantyLog
        fields = '__all__'
        
    def get_remaining_days(self, obj):
        remaining_days = None
        if obj:
            if obj.start_date and obj.end_date:
                today = TODAY
                # today = today + timedelta(days=65)
                remaining_time = obj.end_date - today
                
                if remaining_time > timedelta(days=0):
                    days = remaining_time.days
                    hours, remainder = divmod(remaining_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    remaining_days =  f"{days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds"
                    
        return remaining_days
        
class OrderItemListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    status_color = serializers.SerializerMethodField(read_only =  True)
    product_details = serializers.SerializerMethodField(read_only = True)
    gift_item_details = serializers.SerializerMethodField(read_only = True)
    warranty_details = serializers.SerializerMethodField(read_only = True)
  
    class Meta:
        model = OrderItem
        fields = "__all__"
        
    def get_status_color(self, obj):
        return ORDER_ITEM_STATUS_COLORS.get(obj.status, "#FF0000")
    
    def get_product_details(self, obj):
        context = {}
        if obj.product:
            
            image_url = settings.NOT_FOUND_IMAGE
            
            if obj.product.images:
                image_url = random.choice(obj.product.images)
        
            context  = {
                'id': obj.product.id,
                'name': obj.product.name,
                'slug': obj.product.slug,
                'image': image_url
            }
            
        return context
    
    def get_warranty_details(self, obj):
        if obj.order_item_warranty_logs:
            today = TODAY
            
            warranty_valid_qs = obj.order_item_warranty_logs.filter(end_date__gte = today)
            
            if warranty_valid_qs:
                serializer = OrderItemWarrantyLogSerializer(warranty_valid_qs, many=True)
                return serializer.data
            
        return None
        
    def get_gift_item_details(self, obj):
        context = {}
        if obj.product:
            if obj.product.gift_product:
                
                image_url = settings.NOT_FOUND_IMAGE
                barcode_number = None
                
                if obj.product.gift_product.images:
                    # image_url = obj.product.images[0]
                    image_url = image_url
            
                context  = {
                    'id': obj.product.gift_product.id,
                    'name': obj.product.gift_product.name,
                    'slug': obj.product.gift_product.slug,
                    'image': image_url,
                    'barcode_number': barcode_number,
                }
                
        return context
    
    def get_product_details(self, obj):
        context = {}
        if obj.product:
            
            image_url = settings.NOT_FOUND_IMAGE
            
            if obj.product.images:
                image_url = random.choice(obj.product.images)
        
            context  = {
                'id': obj.product.id,
                'name': obj.product.name,
                'slug': obj.product.slug,
                'logo': image_url
            }
            
        return context
    
class OrderStatusLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusLog
        fields = [
                  'id',
                  'slug',
                  'status_display',
                  'order_status_reason',
                  'status_change_by',
                  'order_status_change_at',
                  ]
        

class OrderDetailsSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only =  True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only =  True)
    status = serializers.SerializerMethodField(read_only = True)
    order_type_display = serializers.CharField(source='get_order_type_display', read_only = True)
    approved_status_display = serializers.CharField(source='get_order_type_display', read_only = True)
    price_details = serializers.SerializerMethodField(read_only = True)
    customer_details = serializers.SerializerMethodField(read_only = True)
    customer_address_details = serializers.SerializerMethodField(read_only = True)
    order_payment_log_details = serializers.SerializerMethodField(read_only = True)
    order_items_details = serializers.SerializerMethodField(read_only = True)
    order_status_log_details = serializers.SerializerMethodField(read_only = True)
    order_status_log_details = serializers.SerializerMethodField(read_only = True)
    shop = OfficeLocationListSerializer(read_only = True)
    pickup_shop = OfficeLocationListSerializer(read_only = True)
    approved_by = UserInformationBaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    delivery_method = DeliveryMethodListSerializer(read_only = True)
    courier_details = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'remarks',
            'order_date',
            'order_approved_date',
            'invoice_no',
            'price_details',
            'status',
            'status_display',
            'payment_status',
            'payment_status_display',
            'payment_type',
            'payment_type_display',
            'approved_status',
            'approved_status_display',
            'order_type',
            'order_type_display',
            'shop',
            'pickup_shop',
            'delivery_method',
            'promo_code',
            'approved_by',
            'customer_details',
            'customer_address_details',
            'order_payment_log_details',
            'order_items_details',
            'order_status_log_details',
            'promo_code',
            'courier_details',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
                  ]
        
        
    def get_status(self, obj):
        status = obj.status
        if obj.status in ['RETURNED', 'GSHEBA_RETURNED']:
            if obj.approved_status in ['APPROVED', 'REJECTED']:
                status = obj.approved_status
                
        elif obj.status in ['SHOP_TO_WAREHOUSE', 'WAREHOUSE_RECEIVED', 'WAREHOUSE_TO_SERVICE_POINT', 'SERVICE_POINT_RECEIVED', 'WAREHOUSE_TO_VENDOR', 'IN_SERVICING', 'SERVICE_POINT_TO_WAREHOUSE']:
            status = obj.status
                
        elif obj.is_for_employee == True and obj.approved_status == "APPROVED":
            status = obj.approved_status
            
        return status
    
    def get_courier_details(self, obj):
        courier_details = None
        id = 1
        name = "Redx"
        
        if obj.couriers:
                try:
                    if obj.couriers.all().last().courier_service:
                        id = obj.couriers.all().last().courier_service.id
                        name = obj.couriers.all().last().courier_service.name
                except:
                    pass
                
        courier_details = {
            'id': id,
            'name': name,
        }
        
        return courier_details
        
    def get_price_details(self, obj):
        context = {}
        # price_details = calculate_order_price(order_obj = obj)
        
        if obj:
            total_due_amount = obj.total_due_amount
            
            if obj.total_due_amount < 0:
                total_due_amount = 0
                
            total_paid_amount = obj.total_advance_amount
                
            qs = OrderPaymentLog.objects.filter(
                order__invoice_no = obj.invoice_no, status = "RECEIVED"
            )
            if qs:
                total_paid_amount = sum(qs.values_list("received_amount", flat=True))
                
            obj.total_paid_amount = total_paid_amount
            obj.save()
            
                
            context = {
                'total_product_price': obj.total_product_price,
                'total_discount_amount': obj.total_discount_amount,
                'total_net_payable_amount': obj.total_net_payable_amount,
                'total_gsheba_amount': obj.total_gsheba_amount,
                'total_tax_amount': obj.total_tax_amount,
                'total_promo_discount': obj.total_promo_discount,
                'total_delivery_charge': obj.total_delivery_charge,
                'total_payable_amount': abs(obj.total_payable_amount),
                # 'total_advance_amount': obj.total_advance_amount,
                'total_advance_amount': total_paid_amount,
                'total_paid_amount': obj.total_paid_amount,
                'total_due_amount': total_due_amount,
                'total_return_amount': obj.total_return_amount,
                'total_expense_amount': obj.total_expense_amount,
                'total_balance_amount': obj.total_balance_amount,
                
                # Refunded
                'refunded_account_holder_name': obj.refunded_account_holder_name,
                'refunded_account_number': obj.refunded_account_number,
                'refunded_amount': obj.refunded_amount,
            }
        
        return context
    
    def get_customer_details(self, obj):
        context = {}
        
        user_type = 'Customer'
        
        if obj.customer.user:
            if obj.customer.user_type:
                user_type = obj.customer.user_type.name
        
        if obj.customer_address_logs.last() and  obj.customer.user:
            customer_info = obj.customer_address_logs.last()
            
            context = {
                'id': obj.customer.user.id,
                'name': customer_info.name,
                'user_type': user_type,
                'email': customer_info.email,
                'phone': customer_info.phone,
                'secondary_phone': customer_info.secondary_phone,
            }
            
        elif obj.customer.user:
            context = {
                'id': obj.customer.user.id,
                'name': obj.customer.name,
                'user_type': user_type,
                'email': obj.customer.user.email,
                'phone': obj.customer.user.phone,
            }
        
        return context

        
    def get_customer_address_details(self, obj):
        context = {}
        
        
        if obj.customer_address_logs.last():
            customer_info = obj.customer_address_logs.last()
            
            if customer_info.address_type == 'HOME':
                address_type_display = 'Home'
            else:
                address_type_display = 'Office'
            
            context = {
                'slug': customer_info.slug,
                'address_type': customer_info.address_type,
                'address_type_display': address_type_display,
                'address': customer_info.address,
                'area_name': customer_info.area_name,
                'district_name': customer_info.district_name,
                'division_name': customer_info.division_name,
                'country_name': customer_info.country_name,
            }
            
        return context

    def get_order_payment_log_details(self, obj):
        if obj.order_payment_logs:
            serializer = OrderPaymentLogListSerializer(obj.order_payment_logs, many = True)
        
        return serializer.data


    def get_order_items_details(self, obj):
        if obj.order_items:
            serializer = OrderItemListSerializer(obj.order_items.filter(is_gift_item = False), many = True)
            # serializer = OrderItemListSerializer(obj.order_items.filter(), many = True)
        
        return serializer.data

    def get_order_status_log_details(self, obj):
        if obj.order_status_logs:
            serializer = OrderStatusLogListSerializer(obj.order_status_logs.order_by('-order_status_change_at'), many = True)
        
        return serializer.data


class CustomerInformationAddressUpdateSerializer(serializers.ModelSerializer):
    order_status_reason = serializers.CharField(required = False) 
    # Customer Info
    name = serializers.CharField(required = False) 
    phone = serializers.CharField(required = False) 
    email = serializers.CharField(required = False) 
    
    # Address
    area_slug = serializers.CharField(required=False)
    address_type = serializers.CharField(required=False)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'order_status_reason',
            'name',
            'phone',
            'email',
            'area_slug',
            'address',
            'address_type',
                  ]
        

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    order_status_reason = serializers.CharField(required = False) 
    order_item_list = OrderItemCreateUpdateSerializer(many= True, write_only = True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'order_status_reason',
            'order_item_list',
                  ]
        

    
class OrderItemStatusLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemStatusLog
        fields = [
                  'id',
                  'status_display',
                  'order_status_reason',
                  'status_change_by',
                  'order_status_change_at',
                  ]
        
        
class OrderItemReturnUpdateSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(required=False)
    status_change_reason = serializers.CharField(required=False)
    order_item_id = serializers.IntegerField(default =1)
    
    barcode_status = serializers.CharField(required = False) 
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order_item_id',
            'status',
            'status_change_reason',
            'product_slug',
            'barcode_number',
            'barcode_status',
                  ]
        
class OrderReturnStatusUpdateSerializer(serializers.ModelSerializer):
    order_status_reason = serializers.CharField(required = False) 
    payment_type = serializers.CharField(required = False) 
    mfs_type = serializers.CharField(required = False) 
    mfs_name = serializers.CharField(required = False) 
    phone_number = serializers.CharField(required = False) 
    bank_name = serializers.CharField(required = False) 
    branch_name = serializers.CharField(required = False) 
    approved_status = serializers.CharField(required = False, default = 'INITIALIZED') 
    order_item_list = OrderItemReturnUpdateSerializer(many= True, write_only = True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'approved_status',
            'refunded_account_holder_name',
            'refunded_account_number',
            'order_status_reason',
            'order_item_list',
            'payment_type',
            'mfs_name',
            'mfs_type',
            'phone_number',
            'bank_name',
            'branch_name',
                  ]
        
class OrderReturnStatusApprovedRejectedSerializer(serializers.ModelSerializer):
    order_status_reason = serializers.CharField(required = False) 
    approved_status = serializers.CharField(required = False, default = 'APPROVED') 
    
    class Meta:
        model = Order
        fields = [
            'approved_status',
            'order_status_reason'
                  ]
        
        
class ServiceOrderItemCreateUpdateSerializer(serializers.ModelSerializer):
    status_change_reason = serializers.CharField(required=False)
    item_id = serializers.IntegerField(default =1)
    
    class Meta:
        model = ServicingOrderItem
        fields = [
            'id',
            'item_id',
            'status',
            'status_change_reason',
                  ]
        
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    order_status_reason = serializers.CharField(required = False) 
    service_order_item_list = ServiceOrderItemCreateUpdateSerializer(many= True, write_only = True)
    
    class Meta:
        model = ServicingOrder
        fields = [
            'id',
            'status',
            'order_status_reason',
            'service_order_item_list',
                  ]
        
        
class ServiceOrderListSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    servicing_type_display = serializers.CharField(source='get_servicing_type_display', read_only =  True)
    customer_details = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = ServicingOrder
        fields = [
            'id',
            'invoice_no',
            'status',
            'status_display',
            'servicing_type',
            'servicing_type_display',
            'order_date',
            'created_by',
            'customer_details',
                  ]
        
    def get_customer_details(self, obj):
        context = {}
        
        image_url = None
        if obj.order.customer:
            image_url = obj.order.customer.image
        
        if obj.order.customer:
            user_type = 'Customer'
            
            if obj.order.customer.user:
                if obj.order.customer.user_type:
                    user_type = obj.order.customer.user_type.name
                    
                if obj.order.customer.name:
                    customer_name = obj.order.customer.name
                    
                else:
                    customer_name = '-'
                    
                context = {
                    'id': obj.order.customer.user.id,
                    'name': customer_name,
                    'user_type': user_type,
                    'email': obj.order.customer.user.email,
                    'phone': obj.order.customer.user.phone,
                    'image': image_url,
                }
        
        return context
        
        
class ServiceOrderItemSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    product = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    class Meta:
        model = ServicingOrderItem
        fields = "__all__"
        
    def get_product(self, obj):
        context = {}
        if obj.product:
            
            image_url = None
            
            if obj.product.images:
                image_url = random.choice(obj.product.images)
        
            context  = {
                'id': obj.product.id,
                'name': obj.product.name,
                'slug': obj.product.slug,
                'image': image_url,
                'barcode': obj.barcode_number
            }
            
        return context
        
class ServiceOrderDetailsSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    servicing_type_display = serializers.CharField(source='get_servicing_type_display', read_only =  True)
    service_order_item_list = serializers.SerializerMethodField(read_only = True)
    customer_details = serializers.SerializerMethodField(read_only = True)
    customer_address_details = serializers.SerializerMethodField(read_only = True)
    order_payment_log_details = serializers.SerializerMethodField(read_only = True)
    price_details = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = ServicingOrder
        fields = "__all__"
        
    def get_service_order_item_list(self, obj):
        if obj.servicing_order_items:
            serializer = ServiceOrderItemSerializer(instance=obj.servicing_order_items, many= True)
            return serializer.data
        # try:
        #     if not obj.servicing_order_items:
        #         order_qs = Order.objects.filter(service_no = obj.invoice_no).last()
        #         order_item_qs = order_qs.order_items.all().filter(status = obj.status)
        #         serializer = OrderItemListSerializer(instance=obj.servicing_order_items, many= True)
        # except:
        #     pass
            
        return None   
    

    def get_order_payment_log_details(self, obj):
        if obj.order.order_payment_logs:
            serializer = OrderPaymentLogListSerializer(obj.order.order_payment_logs, many = True)
        
        return serializer.data
    
    def get_price_details(self, obj):
        context = {}
        price_details = calculate_order_price(order_obj = obj.order)
        
        if obj:
            context = {
                'total_product_price': obj.order.total_product_price,
                'total_discount_amount': obj.order.total_discount_amount,
                'total_net_payable_amount': obj.order.total_net_payable_amount,
                'total_gsheba_amount': obj.order.total_gsheba_amount,
                'total_tax_amount': obj.order.total_tax_amount,
                'total_promo_discount': obj.order.total_promo_discount,
                'total_delivery_charge': obj.order.total_delivery_charge,
                'total_payable_amount': abs(obj.order.total_payable_amount),
                'total_advance_amount': obj.order.total_advance_amount,
                'total_paid_amount': obj.order.total_paid_amount,
                'total_due_amount': obj.order.total_due_amount,
                'total_return_amount': obj.order.total_return_amount,
                'total_expense_amount': obj.order.total_expense_amount,
                'total_balance_amount': obj.order.total_balance_amount,
                
                # Refunded
                'refunded_account_holder_name': obj.order.refunded_account_holder_name,
                'refunded_account_number': obj.order.refunded_account_number,
                'refunded_amount': obj.order.refunded_amount,
            }
        
        return context
        
    def get_customer_details(self, obj):
        context = {}
        
        image_url = None
        if obj.order.customer:
            image_url = obj.order.customer.image
        
        if obj.order.customer:
            user_type = 'Customer'
            
            if obj.order.customer.user:
                if obj.order.customer.user_type:
                    user_type = obj.order.customer.user_type.name
                    
                if obj.order.customer.name:
                    customer_name = obj.order.customer.name
                    
                else:
                    customer_name = '-'
                    
                context = {
                    'id': obj.order.customer.user.id,
                    'name': customer_name,
                    'user_type': user_type,
                    'email': obj.order.customer.user.email,
                    'phone': obj.order.customer.user.phone,
                    'image': image_url,
                }
        
        return context
    
    
        
    def get_customer_address_details(self, obj):
        context = {}
        
        
        if obj.order.customer_address_logs.last():
            customer_info = obj.order.customer_address_logs.last()
            
            if customer_info.address_type == 'HOME':
                address_type_display = 'Home'
            else:
                address_type_display = 'Office'
            
            context = {
                'slug': customer_info.slug,
                'address_type': customer_info.address_type,
                'address_type_display': address_type_display,
                'address': customer_info.address,
                'area_name': customer_info.area_name,
                'district_name': customer_info.district_name,
                'division_name': customer_info.division_name,
                'country_name': customer_info.country_name,
            }
            
        return context
    
class MultipleInvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [ 
            'invoice_no'
        ]
        
    
# class OrderListDownloadSerializer(serializers.ModelSerializer):
#     order_details = serializers.SerializerMethodField(read_only = True)
#     order_item_details = serializers.SerializerMethodField(read_only = True)
#     class Meta:
#         model = OrderItem
#         fields = [
#             'order_details',
#             'order_item_details',
#         ]
        
#     def get_order_details(self, obj):
#         invoice_no = '-'
#         order_date = '-'
#         status = '-'
#         customer_name = '-'
#         customer_phone = '-'
#         customer_email = '-'
#         customer_address = '-'
#         courier_name = '-'
#         shop_name = '-'
#         payment_type = '-'
#         note = '-'
#         payment_status = '-'
#         delivery_type = '-'
#         delivery_method = '-'
#         order_type = '-'
#         total_product_price = 0.0
#         total_discount_amount = 0.0
#         total_net_payable_amount = 0.0
#         total_gsheba_amount = 0.0
#         total_tax_amount = 0.0
#         total_promo_discount = 0.0
#         total_delivery_charge = 0.0
#         total_payable_amount = 0.0
#         total_advance_amount = 0.0
#         total_paid_amount = 0.0
#         total_due_amount = 0.0
        
#         if obj.order:
#             invoice_no = obj.order.invoice_no
#             if obj.order.order_date:
#                 order_date = str(obj.order.order_date.strftime("%b %d, %Y at %I:%M %p") ) or None
#             status = obj.order.status
            
#             if obj.order.customer_address_logs:
#                 customer_name = obj.order.customer_address_logs.last().name
#                 customer_phone = obj.order.customer_address_logs.last().phone
#                 customer_email = obj.order.customer_address_logs.last().email
#                 customer_address = obj.order.customer_address_logs.last().address

        
#         context = {
#             'invoice_no':invoice_no,
#             'order_date':order_date,
#             'status':status,
#             'customer_name':customer_name,
#             'customer_phone':customer_phone,
#             'customer_email':customer_email,
#             'customer_address':customer_address,
#             'courier_name':courier_name,
#             'shop_name':shop_name,
#             'payment_type':payment_type,
#             'note':note,
#             'payment_status':payment_status,
#             'delivery_type':delivery_type,
#             'delivery_method':delivery_method,
#             'order_type':order_type,
#             'total_product_price':total_product_price,
#             'total_discount_amount':total_discount_amount,
#             'total_net_payable_amount':total_net_payable_amount,
#             'total_gsheba_amount':total_gsheba_amount,
#             'total_promo_discount':total_promo_discount,
#             'total_delivery_charge':total_delivery_charge,
#             'total_tax_amount':total_tax_amount,
#             'total_payable_amount':total_payable_amount,
#             'total_advance_amount':total_advance_amount,
#             'total_paid_amount':total_paid_amount,
#             'total_due_amount':total_due_amount,
#         }
        
#         return context
        
#     def get_order_item_details(self, obj):
#         product_name = "-"
#         brand_name = "-"
#         seller_name = "-"
#         product_code = "-"
#         barcode = "-"
#         quantity = "-"
#         msp = 0.0
#         mrp = 0.0
#         selling_price = 0.0
#         promo_discount_amount = 0.0
#         after_promo_discount_selling_price = 0.0
#         promo_code = 0.0
#         commission_amount = 0.0
        
#         print('IIIIIIIIIIIIIIIII', obj)
#         # await asyncio.sleep(1)
        
#         context = {
#             'product_name':product_name,
#             'brand_name':brand_name,
#             'seller_name':seller_name,
#             'product_code':product_code,
#             'barcode':barcode,
#             'quantity':quantity,
#             'msp':msp,
#             'mrp':mrp,
#             'selling_price':selling_price,
#             'promo_discount_amount':promo_discount_amount,
#             'after_promo_discount_selling_price':after_promo_discount_selling_price,
#             'promo_code':promo_code,
#             'commission_amount':commission_amount, 
#         }
#         return context
        
        
class OrderListDownloadSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField(read_only = True)
    order_item_details = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = OrderItem
        fields = [
            'order_details',
            'order_item_details'
            ]
        
    def get_order_details(self, obj):
        invoice_no = '-'
        order_date = '-'
        status = '-'
        customer_name = '-'
        customer_phone = '-'
        customer_email = '-'
        customer_address = '-'
        courier_name = '-'
        shop_name = '-'
        payment_type = '-'
        note = '-'
        payment_status = '-'
        delivery_type = '-'
        delivery_method = '-'
        order_type = '-'
        total_product_price = 0.0
        total_discount_amount = 0.0
        total_net_payable_amount = 0.0
        total_gsheba_amount = 0.0
        total_tax_amount = 0.0
        total_promo_discount = 0.0
        total_delivery_charge = 0.0
        total_payable_amount = 0.0
        total_advance_amount = 0.0
        total_paid_amount = 0.0
        total_due_amount = 0.0
        
        if obj.order:
            invoice_no = obj.order.invoice_no
            if obj.order.order_date:
                order_date = str(obj.order.order_date.strftime("%b %d, %Y at %I:%M %p") ) or None
            status = obj.order.status
            
            if obj.order.customer_address_logs:
                customer_name = obj.order.customer_address_logs.last().name
                customer_phone = obj.order.customer_address_logs.last().phone
                customer_email = obj.order.customer_address_logs.last().email
                customer_address = obj.order.customer_address_logs.last().address

        
        context = {
            'invoice_no':invoice_no,
            'order_date':order_date,
            'status':status,
            'customer_name':customer_name,
            'customer_phone':customer_phone,
            'customer_email':customer_email,
            'customer_address':customer_address,
            'courier_name':courier_name,
            'shop_name':shop_name,
            'payment_type':payment_type,
            'note':note,
            'payment_status':payment_status,
            'delivery_type':delivery_type,
            'delivery_method':delivery_method,
            'order_type':order_type,
            'total_product_price':total_product_price,
            'total_discount_amount':total_discount_amount,
            'total_net_payable_amount':total_net_payable_amount,
            'total_gsheba_amount':total_gsheba_amount,
            'total_promo_discount':total_promo_discount,
            'total_delivery_charge':total_delivery_charge,
            'total_tax_amount':total_tax_amount,
            'total_payable_amount':total_payable_amount,
            'total_advance_amount':total_advance_amount,
            'total_paid_amount':total_paid_amount,
            'total_due_amount':total_due_amount,
        }
        
        return context
        
    def get_order_item_details(self, obj):
        product_name = "-"
        brand_name = "-"
        seller_name = "-"
        product_code = "-"
        barcode = "-"
        quantity = "-"
        msp = 0.0
        mrp = 0.0
        selling_price = 0.0
        promo_discount_amount = 0.0
        after_promo_discount_selling_price = 0.0
        promo_code = 0.0
        commission_amount = 0.0
        
        print('IIIIIIIIIIIIIIIII', obj)
        # await asyncio.sleep(1)
        
        context = {
            'product_name':product_name,
            'brand_name':brand_name,
            'seller_name':seller_name,
            'product_code':product_code,
            'barcode':barcode,
            'quantity':quantity,
            'msp':msp,
            'mrp':mrp,
            'selling_price':selling_price,
            'promo_discount_amount':promo_discount_amount,
            'after_promo_discount_selling_price':after_promo_discount_selling_price,
            'promo_code':promo_code,
            'commission_amount':commission_amount, 
        }
        return context
        
        
class OrderPaymentLogReportSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField(read_only = True)
    order_payment = serializers.SerializerMethodField(read_only = True)
    status_display = serializers.CharField(source='get_status_display', read_only =  True)
    type_display = serializers.CharField(source='get_type_display', read_only =  True)
    class Meta:
        model = OrderPaymentLog
        fields = '__all__'
        
        
    def get_order_details(self, obj):
        invoice_no = '-'
        total_payable_amount = 0.0
        
        if obj.order:
            invoice_no = obj.order.invoice_no
            total_payable_amount = obj.order.total_payable_amount
        
        order_details = {
            'invoice_no': invoice_no,
            'total_payable_amount': total_payable_amount,
        }
        return order_details
        
        
    def get_order_payment(self, obj):
        id = '-'
        name = '-'
        logo = settings.NOT_FOUND_IMAGE
        
        if obj.order_payment:
            id = obj.order_payment.id
            name = obj.order_payment.name
            logo = obj.order_payment.logo
        
        context = {
            'id': id,
            'name': name,
            'logo': logo,
        }
        return context
    
    
# serializers.py

from rest_framework import serializers

class OrderDownloadSerializer(serializers.Serializer):
    # Define fields as per the SQL query result fields
    invoice_no = serializers.CharField()
    order_date = serializers.DateTimeField(format='%b %d, %Y at %I:%M %p')
    status = serializers.CharField()
    approved_status = serializers.CharField()
    customer_username = serializers.CharField()
    delivery_method = serializers.CharField()
    payment_status = serializers.CharField()
    payment_type = serializers.CharField()
    area = serializers.CharField()
    shop = serializers.CharField()
    pickup_shop = serializers.CharField()
    district_name = serializers.CharField()
    division_name = serializers.CharField()
    country_name = serializers.CharField()
    address = serializers.CharField()
    is_active = serializers.BooleanField()
    remarks = serializers.CharField()
    promo_code = serializers.CharField()
    total_product_price = serializers.FloatField()
    total_discount_amount = serializers.FloatField()
    total_net_payable_amount = serializers.FloatField()
    total_gsheba_amount = serializers.FloatField()
    total_tax_amount = serializers.FloatField()
    total_promo_discount = serializers.FloatField()
    total_delivery_charge = serializers.FloatField()
    total_payable_amount = serializers.FloatField()
    total_advance_amount = serializers.FloatField()
    total_paid_amount = serializers.FloatField()
    total_due_amount = serializers.FloatField()
    total_return_amount = serializers.FloatField()
    total_expense_amount = serializers.FloatField()
    total_balance_amount = serializers.FloatField()
    refunded_account_holder_name = serializers.CharField()
    refunded_account_number = serializers.CharField()
    refunded_amount = serializers.FloatField()
    item_status = serializers.CharField()
    quantity = serializers.IntegerField()
    product_name = serializers.CharField()
    unit_msp_price = serializers.FloatField()
    unit_mrp_price = serializers.FloatField()
    selling_price = serializers.FloatField()
    total_product_price_per_item = serializers.FloatField()
    total_tax_amount_per_item = serializers.FloatField()
    total_discount_amount_per_item = serializers.FloatField()
    total_net_price_per_item = serializers.FloatField()
    gsheba_amount = serializers.FloatField()
    commission_amount = serializers.FloatField()
    barcode_number = serializers.CharField()
    promo_code_item = serializers.CharField()
    total_promo_discount_amount_per_item = serializers.FloatField()
    item_is_active = serializers.BooleanField()
    is_gift_item = serializers.BooleanField()
    order_item_id = serializers.IntegerField()
    barcode_status = serializers.CharField()
    item_remarks = serializers.CharField()


class ApplyPromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'promo_code',
            'remarks',
        ]
class CourierServiceAddInOrderSerializer(serializers.Serializer):
    courier_service_slug = serializers.CharField()


class OrderRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'remarks',
        ]