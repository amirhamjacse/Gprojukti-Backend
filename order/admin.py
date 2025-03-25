from django.contrib import admin
from order.models import *

# Register your models here.



class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'delivery_type', 'slug']

    class Meta:
        model = DeliveryMethod
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_no',"customer", "shop", 'pickup_shop', "return_shop",'order_type', 'status', 'approved_status', 'is_for_employee', "delivery_method", 'total_payable_amount', 'created_at']
    
    list_filter = ['shop__name', 'pickup_shop__name', 'return_shop__name']

    search_fields = ['invoice_no', 'customer__name']

    class Meta:
        model = Order
admin.site.register(Order, OrderAdmin)

class CustomerAddressInfoLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order']


    class Meta:
        model = CustomerAddressInfoLog
admin.site.register(CustomerAddressInfoLog, CustomerAddressInfoLogAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'status', 'selling_price', 'gsheba_amount', 'barcode_number', 'is_gift_item', 'order_item_id']
    search_fields = ['order__invoice_no',]
    class Meta:
        model = OrderItem
admin.site.register(OrderItem, OrderItemAdmin)

class OrderPaymentLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order','status', 'transaction_no','order_payment', 'received_amount', 'created_at', 'remarks']
    list_filter = ['order__order_type','order_payment__name']

    class Meta:
        model = OrderPaymentLog
admin.site.register(OrderPaymentLog, OrderPaymentLogAdmin)

class OrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ['order', 'slug','status_display', 'order_status_change_at', 'created_at']

    class Meta:
        model = OrderStatusLog
admin.site.register(OrderStatusLog, OrderStatusLogAdmin)


class OrderItemStatusLogAdmin(admin.ModelAdmin):
    list_display = ['order_item','status_display', 'order_status_change_at', 'created_at']

    class Meta:
        model = OrderItemStatusLog
admin.site.register(OrderItemStatusLog, OrderItemStatusLogAdmin)

class OrderHistoryLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order','status']

    class Meta:
        model = OrderHistoryLog
admin.site.register(OrderHistoryLog, OrderHistoryLogAdmin)

class OrderItemWarrantyLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_item', 'warranty_type', 'warranty_duration','value','start_date', 'end_date']

    class Meta:
        model = OrderItemWarrantyLog
admin.site.register(OrderItemWarrantyLog, OrderItemWarrantyLogAdmin)

class ServicingOrderAdmin(admin.ModelAdmin):
    list_display = ['invoice_no']

    class Meta:
        model = ServicingOrder
admin.site.register(ServicingOrder, ServicingOrderAdmin)

class ServicingOrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ['id']

    class Meta:
        model = ServicingOrderStatusLog
admin.site.register(ServicingOrderStatusLog, ServicingOrderStatusLogAdmin)

class ServicingOrderItemAdmin(admin.ModelAdmin):
    list_display = ['servicing_order', "product", "barcode_number", "created_at"]

    class Meta:
        model = ServicingOrderItem
admin.site.register(ServicingOrderItem, ServicingOrderItemAdmin)

class ServicingOrderItemStatusLogAdmin(admin.ModelAdmin):
    list_display = ['id']

    class Meta:
        model = ServicingOrderItemStatusLog
admin.site.register(ServicingOrderItemStatusLog, ServicingOrderItemStatusLogAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']

    class Meta:
        model = ProductReview
admin.site.register(ProductReview, ProductReviewAdmin)