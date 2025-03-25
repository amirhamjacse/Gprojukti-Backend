from django.db import models 
from user.models import UserAccount
from django.contrib.postgres.fields import ArrayField
from base.models import DAYS, Company

from django.utils.translation import gettext_lazy as _
from utils.generates import unique_slug_generator
from utils.helpers import (
    time_str_mix_slug)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from utils.generates import unique_slug_generator
# from django.contrib.gis.db.models import PointField

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    bn_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='country_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='country_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name  
    
class Division(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    bn_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='divisions')
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='division_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='division_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    bn_name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True, related_name='districts')
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='district_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='district_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name
        

class Area(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    bn_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True, related_name='areas')
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='area_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='area_updated_bys',
        null=True, blank=True)

    def __str__(self):
        try:
            return f"Area Name = {self.name} and District = {self.district.name}"
        except:
            return f"{self.id}"
class POSArea(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    bn_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True,blank=True,related_name='pos_areas')
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='pos_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='pos_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name

class POSRegion(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    bn_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    pos_area = models.ManyToManyField(to=POSArea, blank=True, related_name='pos_regions')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='pos_region_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='pos_region_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name

class OfficeLocation(models.Model):
    OFFICE_TYPE = [
        ('HEAD_OFFICE', "Head Office"),
        ('WAREHOUSE', "Warehouse"),
        ('BRANCH', "Branch"),
        ('STORE', "Store"),
        ('OTHERS', "Others"),
    ]
    name = models.CharField(max_length=550)
    slug = models.SlugField(max_length=255,unique=True)
    store_no = models.CharField(max_length=10, blank=True, null=True)
    bn_name = models.CharField(max_length=100,null=True)
    address = models.TextField(null=False)
    primary_phone = models.CharField(max_length=17)
    email = models.CharField(max_length=50, blank=True, null=True)
    # location = PointField(geography=True, default=Point(0.0, 0.0))
    map_link = models.URLField()
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='locations')
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='locations')
    office_type = models.CharField(
        choices=OFFICE_TYPE, max_length=50, default="STORE")
    is_shown_in_website = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_use_scanner = models.BooleanField(default=True)
    
    off_days = ArrayField(models.CharField(choices = DAYS, max_length=50),
                          blank=True, default=list)
    pos_area_name = models.CharField(max_length=150, blank=True, null=True) # Auto Generated From Area
    pos_region_name = models.CharField(max_length=150, blank=True, null=True) # Auto Generated From POS Area
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='office_location_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='office_location_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        return str(self.id)
    
    class Meta:
        ordering = ['-name']

    
