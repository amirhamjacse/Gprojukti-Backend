from django.db import models

# from courier_management.models import *
from user.models import UserAccount, UserInformation
from location.models import Area, OfficeLocation
from base.models import *
from product_management.models.product import Product
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class DeliveryMethod(models.Model):
    TYPE = [
        ("HOME_DELIVERY", "Home Delivery"),
        ("STORE_SELL", "Store Sell"),
        ("SHOP_PICKUP", "Shop Pickup"),
        ("EXPRESS_HOME_DELIVERY_INSIDE_DHAKA", "Express Home Delivery Inside Dhaka"),
        ("EXPRESS_HOME_DELIVERY_OUTSIDE_DHAKA", "Express Home Delivery Outside Dhaka"),
        ("EXPRESS_DELIVERY_FROM_STORE_PICKUP_INSIDE_DHAKA", "Express Delivery From Store Pickup Inside Dhaka"),
        ("EXPRESS_DELIVERY_FROM_STORE_PICKUP_OUTSIDE_DHAKA", "Express Delivery From Store Pickup Outside Dhaka"),
        ("INSIDE_DHAKA", "Inside Dhaka"),
        ("OUTSIDE_DHAKA", "Outside Dhaka"),
        ("SAME_DAY_DELIVERY", "Same Day Delivery"),
        ("SHOP_TO_HOME_DELIVERY", "Shop To Home Delivery"),
    ]
    
    delivery_type = models.CharField(max_length=150, choices=TYPE)
    slug = models.SlugField(max_length=255,unique=True)
    delivery_charge = models.FloatField(default = 0.0)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='delivery_method_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='delivery_method_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.delivery_type:
            return str(self.delivery_type)
        return str(self.id)
    
    
class Order(models.Model):
    invoice_no = models.CharField(max_length=150, unique = True)
    service_no = models.CharField(max_length=150, blank=True, null=True) # This Variable is Use, When Order is In Servicing
    order_type = models.CharField(max_length=150, 
                                  choices=ORDER_TYPE, default= "ECOMMERCE_SELL")
    status = models.CharField(max_length=150, 
                              choices=ORDER_STATUS, default= "ORDER_RECEIVED")
    approved_status = models.CharField(max_length=150, 
                              choices=ORDER_APPROVED_STATUS, default= "APPROVED")
    customer = models.ForeignKey(
        UserInformation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='orders')
    delivery_method = models.ForeignKey(
        DeliveryMethod, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='orders')
    payment_status = models.CharField(max_length=150, 
                              choices=PAYMENT_STATUS, default= "UNPAID")
    payment_type = models.CharField(max_length=150, 
                              choices=PAYMENT_TYPE, 
                              default= "CASH_ON_DELIVERY")
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='orders')
    shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='orders')
    pickup_shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='pickup_shop_orders')
    return_shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='return_shop_orders')
    district_name = models.CharField(max_length=150,null=True, blank=True)
    division_name = models.CharField(max_length=150,null=True, blank=True)
    country_name = models.CharField(max_length=150,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_for_employee = models.BooleanField(default=False)
    
    remarks = models.TextField(null=True, blank=True)
    
    promo_code = models.CharField(max_length=150, null=True, blank=True)
    
    # Order Calculation
    
    total_product_price = models.FloatField(default=0.0)
    total_discount_amount = models.FloatField(default=0.0)
    total_net_payable_amount = models.FloatField(default=0.0) # total_product_price - total_discount_amount
    total_gsheba_amount = models.FloatField(default=0.0)
    total_tax_amount = models.FloatField(default=0.0)
    total_promo_discount = models.FloatField(default=0.0)
    total_delivery_charge = models.FloatField(default=0.0)
    total_payable_amount = models.FloatField(default=0.0) # (total_net_payable_amount + total_gsheba_amount + total_tax_amount + total_delivery_charge) - total_promo_discount
    
    total_advance_amount = models.FloatField(default=0.0)
    total_paid_amount = models.FloatField(default=0.0) # total_advance_amount + total_paid_amount
    
    total_due_amount = models.FloatField(default=0.0) # total_payable_amount - total_paid_amount
    total_return_amount = models.FloatField(default=0.0) # If In this Order Any Item Return Then Add
    total_expense_amount = models.FloatField(default=0.0) # Manually Add
    total_balance_amount = models.FloatField(default=0.0) # total_payable_amount - total_return_amount - total_expense_amount
    
    # When Order Amount is Refunded
    refunded_account_holder_name = models.CharField(max_length=350, blank=True, null=True)
    refunded_account_number = models.CharField(max_length=150,blank=True, null=True)
    refunded_amount = models.FloatField(default = 0.0)
    
    order_date = models.DateTimeField(blank=True, null=True)
    order_approved_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='orders', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.invoice_no)
    
    # def save(self, *args, **kwargs):
    #     qs = OrderPaymentLog.objects.filter(order__invoice_no = self.invoice_no)
        
    #     self.total_paid_amount = sum(qs.values_list("received_amount", flat=True))
    #     super().save(*args, **kwargs)
    

    
class CustomerAddressInfoLog(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE ,related_name='customer_address_logs')
    slug = models.SlugField(max_length=255,unique=True)
    address_type = models.CharField(max_length=150, 
                                  choices=ADDRESS_TYPE, default= "HOME")
    name = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=50)
    secondary_phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=350, null=True, blank=True)
    address = models.CharField(max_length=350, null=True, blank=True)
    
    area_name = models.CharField(max_length=350,null=True, blank=True)
    district_name = models.CharField(max_length=350,null=True, blank=True)
    division_name = models.CharField(max_length=350,null=True, blank=True)
    country_name = models.CharField(max_length=350,null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='customer_address_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='customer_address_log_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        return str(self.order.invoice_no)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_items')
    status = models.CharField(max_length=550, 
                              choices=ORDER_ITEM_STATUS, default= "ORDER_RECEIVED")
    quantity = models.IntegerField(default = 1)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_items')
    unit_msp_price = models.FloatField(default = 0.0)
    unit_mrp_price = models.FloatField(default = 0.0)
    selling_price = models.FloatField(default = 0.0) # This is Price which is Actually Sold
    total_product_price = models.FloatField(default = 0.0) # selling_price * quantity
    total_tax_amount = models.FloatField(default = 0.0) # product * quantity
    total_discount_amount = models.FloatField(default = 0.0) # product * quantity
    discount_value = models.FloatField(default = 0.0) 
    discount_type = models.CharField(max_length=150,null=True, blank=True) #  Flat Or Percentage 
    total_net_price = models.FloatField(default = 0.0) # total_product_price - total_discount_amount
    gsheba_amount = models.FloatField(default = 0.0)
    commission_amount = models.FloatField(default = 0.0)
    barcode_number = models.CharField(max_length=150 ,null=True, blank=True)
    promo_code = models.CharField(max_length=150 ,null=True, blank=True)
    total_promo_discount_amount = models.FloatField(default = 0.0) # product * quantity
    promo_discount_value = models.FloatField(default = 0.0) 
    promo_discount_type = models.CharField(max_length=150,null=True, blank=True) #  Flat Or Percentage 
    is_active = models.BooleanField(default=True)
    # If Has Any Gift Item That Add
    is_gift_item = models.BooleanField(default=False)
    order_item_id = models.IntegerField(default = 0.0)
    barcode_status = models.CharField(max_length=150 ,null=True, blank=True) # This Key is for Order Item return
    
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_item_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_item_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        name = f"Invoice No = {self.order} and Order Item ID = {self.id}"
        return str(name)
    
    
class OrderPaymentLog(models.Model):
    transaction_no = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=150, 
                              choices=ORDER_PAYMENT_STATUS, default= "RECEIVED")
    account_number = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255,unique=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_payment_logs')
    order_payment = models.ForeignKey(
        PaymentType, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_payment_logs')
    order_status = models.CharField(max_length=150)
    received_amount = models.FloatField(default = 0.0)
    
    # For Refunded
    
    refunded_account_name = models.CharField(max_length=150,blank=True, null=True)
    refunded_account_number = models.CharField(max_length=150,blank=True, null=True)
    bank_name = models.CharField(max_length=150,blank=True, null=True)
    routing_number = models.CharField(max_length=150,blank=True, null=True)
    type = models.CharField(max_length=150, 
                              choices=ORDER_PAYMENT_TYPE, default= "PERSONAL")
    
    remaining_amount = models.FloatField(default = 0.0)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_payment_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_payment_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.order:
            return str(self.order.invoice_no)
        return str(self.id)
    

class OrderStatusLog(models.Model):
    slug = models.SlugField(max_length=255,unique=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_status_logs')
    status = models.CharField(max_length=150)
    status_display = models.CharField(max_length=150)
    order_status_reason = models.TextField(null=True, blank=True)
    status_change_by = models.JSONField(blank=True, null=True)
    order_status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.order.invoice_no)
    
class OrderItemStatusLog(models.Model):
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_item_status_logs')
    status = models.CharField(max_length=150)
    status_display = models.CharField(max_length=150)
    order_status_reason = models.TextField(null=True, blank=True)
    status_change_by = models.JSONField(blank=True, null=True)
    order_status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_item_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_item_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.order_item)
 
    
class OrderItemWarrantyLog(models.Model):
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_item_warranty_logs')
    warranty_type = models.CharField(max_length=30, choices=WARRANTY_TYPE, default = "GSHEBA_WARRANTY")
    value = models.CharField(max_length=30)
    warranty_duration = models.CharField(max_length=50, choices=WARRANTY_DURATION, default = "MONTH")
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    remaining_days = models.CharField(max_length=230, null=True, blank=True)
    status_change_by = models.JSONField(blank=True, null=True)
    order_status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_item_warranty_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_item_warranty_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.order_item)
    

class OrderHistoryLog(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL ,null=True, blank=True,related_name='order_history_logs')
    
    invoice_no = models.CharField(max_length=150, unique = True)
    order_type = models.CharField(max_length=150, 
                                  choices=ORDER_TYPE, default= "ECOMMERCE_SELL")
    status = models.CharField(max_length=150, 
                              choices=ORDER_STATUS, default= "ORDER_RECEIVED")
    customer_info = models.JSONField(blank=True, null=True)
    delivery_method = models.CharField(max_length=150, blank=True, null=True)
    
    payment_status = models.CharField(max_length=150, 
                              choices=PAYMENT_STATUS, default= "UNPAID")
    
    payment_type = models.CharField(max_length=150, blank=True, null=True, choices=PAYMENT_TYPE)
    
    full_address = models.TextField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    promo_code_info = models.JSONField(blank=True, null=True)
    order_item_info = models.JSONField(blank=True, null=True)
    order_status_info = models.JSONField(blank=True, null=True)
    courier_info = models.JSONField(blank=True, null=True) 
    
    # Order Calculation
    
    total_product_price = models.FloatField(default=0.0)
    total_discount_amount = models.FloatField(default=0.0)
    total_net_payable_amount = models.FloatField(default=0.0) # total_product_price - total_discount_amount
    total_gsheba_amount = models.FloatField(default=0.0)
    total_tax_amount = models.FloatField(default=0.0)
    total_promo_discount = models.FloatField(default=0.0)
    total_delivery_charge = models.FloatField(default=0.0)
    total_payable_amount = models.FloatField(default=0.0) # (total_net_payable_amount + total_gsheba_amount + total_tax_amount + total_delivery_charge) - total_promo_discount
    
    total_advance_amount = models.FloatField(default=0.0)
    total_paid_amount = models.FloatField(default=0.0) # total_advance_amount + total_paid_amount
    
    total_due_amount = models.FloatField(default=0.0) # total_payable_amount - total_paid_amount
    total_return_amount = models.FloatField(default=0.0) # If In this Order Any Item Return Then Add
    total_expense_amount = models.FloatField(default=0.0) # Manually Add
    total_balance_amount = models.FloatField(default=0.0) # total_payable_amount - total_return_amount - total_expense_amount
    
    order_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='order_history_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='order_history_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.invoice_no)
    
# Service System
class ServicingOrder(models.Model):
    invoice_no = models.CharField(max_length=150, unique = True)
    status = models.CharField(max_length=150, 
                              choices=ORDER_STATUS, default= "ORDER_RECEIVED")
    servicing_type = models.CharField(max_length=150, 
                              choices=SERVICING_TYPE, default= "SERVICE")
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL ,null=True, blank=True,related_name='servicing_orders')
    
    order_date = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='servicing_order_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='servicing_order_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.invoice_no)
    

class ServicingOrderStatusLog(models.Model):
    slug = models.SlugField(max_length=255,unique=True)
    servicing_order = models.ForeignKey(
        ServicingOrder, on_delete=models.SET_NULL ,null=True, blank=True,related_name='servicing_order_status_logs')
    status = models.CharField(max_length=150)
    status_display = models.CharField(max_length=150)
    order_status_reason = models.TextField(null=True, blank=True)
    status_change_by = models.JSONField(blank=True, null=True)
    order_status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='servicing_order_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='servicing_order_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.servicing_order.invoice_no)
class ServicingOrderItem(models.Model):
    servicing_order = models.ForeignKey(
        ServicingOrder, on_delete=models.SET_NULL ,null=True, blank=True,related_name='servicing_order_items')
    status = models.CharField(max_length=150, 
                              choices=ORDER_ITEM_STATUS, default= "ORDER_RECEIVED")
    quantity = models.IntegerField(default = 1)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL ,null=True, blank=True,related_name='servicing_order_items')
    
    barcode_number = models.CharField(max_length=150 ,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='servicing_order_item_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='servicing_order_item_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        name = f"Invoice No = {self.servicing_order} and Order Item ID = {self.id}"
        return str(name)
    
    
class ServicingOrderItemStatusLog(models.Model):
    servicing_order_item = models.ForeignKey(
        ServicingOrderItem, on_delete=models.SET_NULL ,null=True, blank=True,related_name='servicing_order_item_status_logs')
    status = models.CharField(max_length=150)
    status_display = models.CharField(max_length=150)
    order_status_reason = models.TextField(null=True, blank=True)
    status_change_by = models.JSONField(blank=True, null=True)
    order_status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='servicing_order_item_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='servicing_order_item_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.servicing_order_item)
 
 

class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_reviews'
        )
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_reviews'
        )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(null=True, blank=True)
    
    is_show_in_ecommerce = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_review_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_review_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.servicing_order_item)