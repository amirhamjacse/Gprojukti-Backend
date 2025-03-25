from django.db import models

from human_resource_management.models.employee import EmployeeInformation
from location.models import OfficeLocation
from product_management.models.category import Category
from product_management.models.product import Product
from user.models import UserAccount

# Create your models here.


class Slider(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=255,unique=True)
    image = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='sliders')
    serial_no = models.IntegerField(default = 1)
    is_popup = models.BooleanField(default = False)
    is_slider = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='slider_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='slider_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
    
    
 
class ShopDayEnd(models.Model):
    shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='shop_day_ends'
        )
    slug = models.SlugField(max_length=255,unique=True)
    total_sell_amount = models.FloatField(default = 0.0)
    retail_sell_amount = models.FloatField(default = 0.0)
    retail_gsheba_sell_amount = models.FloatField(default = 0.0)
    panel_partnership = models.JSONField(null=True, blank=True)  #
    e_retail_sell_amount = models.FloatField(default = 0.0) 
    ecommerce_collection_amount = models.FloatField(default = 0.0) 
    corporate_sell_amount = models.FloatField(default = 0.0) 
    refund_amount = models.FloatField(default = 0.0)
    warranty_claim_quantity = models.FloatField(default = 0.0) 
    gsheba_claim_quantity = models.FloatField(default = 0.0) 
    total_b2b_sell_amount = models.FloatField(default = 0.0) 
    mfs_collection = models.JSONField(null=True, blank=True)
    currency_collection = models.JSONField(null=True, blank=True) 
    total_bank_deposit_amount = models.FloatField(default = 0.0) 
    total_expense_amount = models.FloatField(default = 0.0) 
    
    petty_cash_amount = models.FloatField(default = 0.0) 
    opening_balance_amount = models.FloatField(default = 0.0) 
    current_balance_amount = models.FloatField(default = 0.0) 
    
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    
    day_end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='shop_day_end_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='shop_day_end_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.shop:
            return self.shop.name
        else:
            return str(self.id)

class ShopDayEndMessage(models.Model):
    office_location = models.ManyToManyField(
        to=OfficeLocation, 
        blank=True, related_name='shop_day_end_messages'
        )
    employee_information = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='shop_day_end_messages'
        )
    is_message_send = models.BooleanField(default=True)
    is_mail_send = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='shop_day_end_message_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='shop_day_end_message_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.employee_information:
            return self.employee_information.name
        else:
            return str(self.id)
        
class NewsLetter(models.Model):
    email = models.CharField(max_length=50)
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='newsletter_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='newsletter_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.email:
            return self.email
        else:
            return str(self.id)
        


class ShopPanel(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=150)
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='shop_panel_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='shop_panel_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
        
class ShopPanelHook(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=150)
    serial_no = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    shop_panel = models.ForeignKey(
        ShopPanel, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='shop_panel_hooks'
        )
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='shop_panel_hook_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='shop_panel_hook_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
        
class HookProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='hook_products'
        ) 
    shop_panel_hook = models.ForeignKey(
        ShopPanelHook, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='hook_products'
        ) 
    slug = models.CharField(max_length=150)
    serial_no = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='hook_product_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='hook_product_updated_bys',
        null=True, blank=True)
    
    
    # def __str__(self):
    #     if self.product:
    #         return self.product.name
    #     else:
    #         return str(self.id)