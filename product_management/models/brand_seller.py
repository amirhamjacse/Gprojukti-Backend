from django.db import models
from user.models import UserAccount
from base.models import Company
from django.utils.translation import gettext_lazy as _
from discount.models import Discount

# Create your models here.


TYPE = [
        ('BANGLADESHI', 'Bangladeshi'),
        ('INTERNATIONAL', 'International')
    ]
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    logo = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    is_show_in_ecommece = models.BooleanField(default=True)
    is_show_in_pos = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
#     """ For SEO Friendly for Operations """
    
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    canonical = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='brand_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='brand_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-id"]
     
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    logo = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    is_show_in_ecommece = models.BooleanField(default=True)
    is_show_in_pos = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=TYPE, default='BANGLADESHI')
    
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE ,related_name='suppliers',
        blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
#     """ For SEO Friendly for Operations """
    
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    canonical = models.URLField(null=True, blank=True)
    # banner_image = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='supplier_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='supplier_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
     

     
class Seller(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    logo = models.URLField(blank=True, null=True)
    registration_no = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE, default='BANGLADESHI')
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_person = models.JSONField(default=dict)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE ,related_name='sellers',
        blank=True, null=True)
    paid_amount = models.FloatField(default=0.0)
    due_amount = models.FloatField(default=0.0)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='seller_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='seller_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
     