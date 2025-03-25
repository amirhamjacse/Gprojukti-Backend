from django.db import models
from user.models import UserAccount, UserInformation
from base.models import ORDER_TYPE, Company

# Create your models here.

class Discount(models.Model):
    SCHEDULE_TYPE = [
        ("DATE_WISE", "Date Wise"),
        ("TIME_WISE", "Time Wise")
    ]
    AMOUNT_TYPE = [
        ("PERCENTAGE", "Percentage"),
        ("FLAT", "Flat")
    ]
    DISCOUNT_TYPE = [
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline")
    ]
    DISCOUNT_STATUS = [
        ("CAMPAIGN", "Campaigns"),
        ("DEAL_OF_WEEK", "Deal of the week"),
        ("DISCOUNT", "Discount")
    ]
    name = models.CharField(max_length=350)
    slug = models.SlugField(max_length=255,unique=True)
    image = models.URLField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_TYPE, default='DATE_WISE')
    amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE, default='FLAT')
    discount_amount = models.FloatField(default = 0.0)
    discount_type = models.CharField(max_length=100, choices=ORDER_TYPE, default='ECOMMERCE_SELL')
    discount_status = models.CharField(max_length=20, choices=DISCOUNT_STATUS, default='DISCOUNT')
    is_for_lifetime = models.BooleanField(default = False)
    meta = models.JSONField(default=dict, blank=True, null=True)
    terms_and_conditions = models.TextField(null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='discounts')
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='discount_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='discount_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
    

class PromoCode(models.Model):
    SCHEDULE_TYPE = [
        ("DATE_WISE", "Date Wise"),
        ("TIME_WISE", "Time Wise")
    ]
    AMOUNT_TYPE = [
        ("PERCENTAGE", "Percentage"),
        ("FLAT", "Flat")
    ]
    promo_code = models.CharField(max_length=350, unique =  True)
    slug = models.SlugField(max_length=255,unique=True)
    image = models.URLField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_TYPE, default='DATE_WISE')
    amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE, default='FLAT')
    discount_amount = models.FloatField(default = 0.0)
    promo_type = models.CharField(max_length=150, 
                                  choices=ORDER_TYPE, default= "ECOMMERCE_SELL")
    is_for_lifetime = models.BooleanField(default = False)
    is_for_all = models.BooleanField(default = False) # This is for All Type of Order
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='promo_codes')
    remarks = models.TextField(null=True, blank=True)
    minimum_purchase_amount = models.FloatField(default = 0.0)
    maximum_purchase_amount = models.FloatField(default = 0.0)
    maximum_use_limit = models.PositiveIntegerField(default = 0)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='promo_code_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='promo_code_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.promo_code:
            return self.promo_code
        else:
            return str(self.id)
    

    
class PromoCodeLog(models.Model):
    customer = models.ForeignKey(UserInformation,
                                  on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='promo_code_logs')
    promo_code = models.ForeignKey(PromoCode,
                                  on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='promo_code_logs')
    slug = models.SlugField(max_length=255,unique=True)
    total_apply = models.IntegerField(default =0)
    applied_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='promo_code_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='promo_code_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
