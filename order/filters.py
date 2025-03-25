import django_filters
from order.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone
from datetime import datetime

from product_management.models.product import ProductStock


class OrderFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")
    order_type = django_filters.CharFilter(label="order_type",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    payment_status = django_filters.CharFilter(label="payment_status",
                                         method="filter_model")
    is_for_employee = django_filters.CharFilter(label="is_for_employee",
                                         method="filter_model")
    office_location = django_filters.CharFilter(label="office_location",
                                         method="filter_model")

    class Meta:
        model = Order
        fields = (
            'search',
            'status',
            'order_type',
            'start_date',
            'end_date',
            'payment_status',
            'is_for_employee',
            'office_location',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        status = self.data.get('status')
        order_type = self.data.get('order_type')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        payment_status = self.data.get('payment_status')
        is_for_employee = self.data.get('is_for_employee')
        office_location = self.data.get('office_location')
        
        if search:
            queryset = queryset.filter(
                Q(invoice_no__icontains = search)
                | Q(customer_address_logs__name__icontains = search)
                | Q(customer_address_logs__phone__icontains = search)
                | Q(customer_address_logs__email__icontains = search)
                | Q(customer_address_logs__address__icontains = search)
                | Q(customer_address_logs__area_name__icontains = search)
                | Q(customer_address_logs__district_name__icontains = search)
                | Q(customer_address_logs__division_name__icontains = search)
                | Q(customer_address_logs__country_name__icontains = search)
                | Q(order_items__barcode_number__icontains = search)
            )
            
        if office_location:
            queryset = queryset.filter(
                Q(shop__name__icontains = office_location)
                | Q(shop__slug__icontains = office_location)
            )
            
        if status:
            queryset = queryset.filter(
                status = status
                )
        if order_type:
            queryset = queryset.filter(
                order_type = order_type
            )
            
        if payment_status:
            queryset = queryset.filter(
                payment_status = payment_status
                )
            
        if start_date and end_date:
            queryset = queryset.filter(
                order_date__date__range=(start_date, end_date)
            )
            
        if is_for_employee:
            if is_for_employee.lower() == 'true' :
                queryset = queryset.filter(
                    is_for_employee = True 
                )
            else:
                queryset = queryset.filter(
                    is_for_employee = False 
                )
            
        queryset = queryset.distinct()
        
        return queryset
   

class OrderReportFilter(django_filters.FilterSet):
    is_online = django_filters.CharFilter(label="is_online",
                                         method="filter_model")
    is_offline = django_filters.CharFilter(label="is_offline",
                                         method="filter_model") 

    class Meta:
        model = Order
        fields = (
            'is_online',
            'is_offline',
            )

    def filter_model(self, queryset, name, value):
        is_online = self.data.get('is_online')
        is_offline = self.data.get('is_offline')
         
        if is_online:
            if is_online.lower() == 'true':
                queryset = queryset.filter(
                    order_type__in = ["ECOMMERCE_SELL", "RETAIL_ECOMMERCE_SELL"]
            )
        if is_offline:
            if is_offline.lower() == 'true':
                queryset = queryset.filter(
                    order_type__in = ["POINT_OF_SELL", "ON_THE_GO"]
                )
            
        return queryset
    
# class OrderItemReportFilter(django_filters.FilterSet):
#     is_online = django_filters.CharFilter(label="is_online",
#                                          method="filter_model")
#     is_offline = django_filters.CharFilter(label="is_offline",
#                                          method="filter_model") 

#     class Meta:
#         model = OrderItem
#         fields = (
#             'is_online',
#             'is_offline',
#             )

#     def filter_model(self, queryset, name, value):
#         is_online = self.data.get('is_online')
#         is_offline = self.data.get('is_offline')
         
#         if is_online:
#             queryset = queryset.filter(
#                 order__order_type__in = ["ECOMMERCE_SELL", "RETAIL_ECOMMERCE_SELL"]
#             )
#         if is_online:
#             queryset = queryset.filter(
#                 order__order_type__in = ["POINT_OF_SELL", "ON_THE_GO"]
#             )
            
#         return queryset

class OrderItemReportFilter(django_filters.FilterSet):
    # is_online = django_filters.CharFilter(label="is_online",
    #                                      method="filter_model")
    # is_offline = django_filters.CharFilter(label="is_offline",
    #                                      method="filter_model")
    payment_status = django_filters.CharFilter(label="payment_status",
                                         method="filter_model") 
    order_type = django_filters.CharFilter(label="order_type",
                                         method="filter_model") 
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")  
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")  
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")  
    status = django_filters.CharFilter(label="status",
                                         method="filter_model") 
    shop = django_filters.CharFilter(label="shop",
                                         method="filter_model") 

    class Meta:
        model = OrderItem
        fields = (
            'search',
            'payment_status',
            'order_type',
            'start_date',
            'end_date',
            'status',
            'shop',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        is_online = self.data.get('is_online')
        is_offline = self.data.get('is_offline')
        payment_status = self.data.get('payment_status')
        order_type = self.data.get('order_type')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        status = self.data.get('status')
        shop = self.data.get('shop')
         
        if is_online:
            queryset = queryset.filter(
                order__order_type__in = ["ECOMMERCE_SELL", "RETAIL_ECOMMERCE_SELL"]
            )
        if is_online:
            queryset = queryset.filter(
                order__order_type__in = ["POINT_OF_SELL", "ON_THE_GO"]
            )
            
        if payment_status:
            queryset = queryset.filter(
                order__payment_status = payment_status
            )
            
        if status:
            queryset = queryset.filter(
                Q(status = status)
                | Q(order__status = status)
            )
            
        if shop:
            queryset = queryset.filter(
                Q(order__shop__name__icontains = shop)
                | Q(order__shop__slug__icontains = shop)
            )
            
        if order_type:
            queryset = queryset.filter(
                order__order_type = order_type
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                order__order_date__date__range=(start_date, end_date)
            )
            
        if search:
            queryset = queryset.filter(
                Q(order__invoice_no__icontains = search)
                | Q(order__service_no__icontains = search)
                | Q(order__customer__name__icontains = search)
                | Q(order__customer__user__email__icontains = search)
                | Q(order__customer__user__phone__icontains = search)
            )
            
        return queryset

class TopProductSellReportFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model") 
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model") 
    supplier = django_filters.CharFilter(label="supplier",
                                         method="filter_model") 
    brand = django_filters.CharFilter(label="brand",
                                         method="filter_model") 
    shop = django_filters.CharFilter(label="shop",
                                         method="filter_model") 

    class Meta:
        model = Product
        fields = (
            'search',
            'start_date',
            'end_date',
            'supplier',
            'brand',
            'shop',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        supplier = self.data.get('supplier')
        brand = self.data.get('brand')
        shop = self.data.get('shop')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                # | Q(product_parent__name__icontains = search)
                # | Q(product_parent__slug__icontains = search)
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                order_items__order__order_date__date__range=(start_date, end_date)
            )
            
        if supplier:
            queryset = queryset.filter(
                Q(supplier__name__icontains = supplier)
                | Q(supplier__slug__icontains = supplier)
            )
            
        if brand:
            queryset = queryset.filter(
                Q(brand__name__icontains = brand)
                | Q(brand__slug__icontains = brand)
            )
            
        if shop:
            queryset = queryset.filter(
                Q(order_items__order__shop__name__icontains = shop)
                | Q(order_items__order__shop__slug__icontains = shop)
            )
            
        return queryset.distinct()
    
class OrderPaymentLogReportFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model") 
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model") 
    status = django_filters.CharFilter(label="status",
                                         method="filter_model") 
    payment_method = django_filters.CharFilter(label="payment_method",
                                         method="filter_model") 

    class Meta:
        model = OrderPaymentLog
        fields = (
            'search',
            'start_date',
            'end_date',
            'status',
            'payment_method',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        status = self.data.get('status')
        payment_method = self.data.get('payment_method')
            
        if search:
            queryset = queryset.filter(
                Q(transaction_no__icontains = search)
                | Q(account_number__icontains = search)
                | Q(slug__icontains = search)
                | Q(order__invoice_no__icontains = search)
                | Q(order_status__icontains = search)
                | Q(received_amount__icontains = search)
                | Q(refunded_account_name__icontains = search)
                | Q(bank_name__icontains = search)
                | Q(routing_number__icontains = search)
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__date__range=(start_date, end_date)
            )
            
        if status:
            queryset = queryset.filter(
                Q(status__icontains = status)
            )
            
        if payment_method:
            queryset = queryset.filter(
                Q(order_payment__name__icontains = payment_method)
                | Q(order_payment__slug__icontains = payment_method)
            )
            
        return queryset
    
    


class ProductStockReportFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model") 
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model") 
    status = django_filters.CharFilter(label="status",
                                         method="filter_model") 
    supplier = django_filters.CharFilter(label="supplier",
                                         method="filter_model") 
    brand = django_filters.CharFilter(label="brand",
                                         method="filter_model") 
    stock_location = django_filters.CharFilter(label="stock_location",
                                         method="filter_model") 

    class Meta:
        model = ProductStock
        fields = (
            'search',
            'start_date',
            'end_date',
            'status',
            'supplier',
            'brand',
            'stock_location',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        supplier = self.data.get('supplier')
        brand = self.data.get('brand')
        status = self.data.get('status')
        stock_location = self.data.get('stock_location')
        
        if search:
            queryset = queryset.filter(
                Q(barcode__icontains = search)
                | Q(product_price_info__product__name__icontains = search)
                | Q(product_price_info__product__slug__icontains = search)
                | Q(product_price_info__product__product_code__icontains = search)
            )
            
        if start_date:
            queryset = queryset.filter(
                stock_in_date__date = start_date
            )
        if end_date:
            queryset = queryset.filter(
                stock_in_date__date = end_date
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                stock_in_date__date__range=(start_date, end_date)
            )
            
        if status:
            queryset = queryset.filter(
                status =  status
            )
            
        if supplier:
            queryset = queryset.filter(
                Q(product_price_info__product__supplier__name__icontains = supplier)
                | Q(product_price_info__product__supplier__slug__icontains = supplier)
            )
            
        if brand:
            queryset = queryset.filter(
                Q(product_price_info__product__brand__name__icontains = brand)
                | Q(product_price_info__product__brand__slug__icontains = brand)
            )
            
        if stock_location:
            queryset = queryset.filter(
                Q(stock_location__name__icontains = stock_location)
                | Q(stock_location__slug__icontains = stock_location)
            )
            
        return queryset.distinct()