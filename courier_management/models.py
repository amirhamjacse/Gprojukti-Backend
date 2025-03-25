from django.db import models
from base.models import COURIER_STATUS, Company
from order.models import Order
from user.models import UserAccount
# from order.models import *
from human_resource_management.models.employee import EmployeeInformation

# Create your models here.

class CourierService(models.Model):
    COURIER_TYPE = [
        ("IN_HOUSE", "In-House"),
        ("THIRD_PARTY", "Third Party"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255,unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    meta = models.JSONField(default=dict)
    courier_type = models.CharField(max_length=30, 
                                    choices=COURIER_TYPE, default="IN_HOUSE")
    
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='delivery_mans')
    is_active = models.BooleanField(default=True)
    remarks =  models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='courier_service_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='courier_service_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name
    
class DeliveryMan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255,unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    courier_service = models.ForeignKey(
        CourierService, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='delivery_mans')
    employee = models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='delivery_mans')
    
    is_active = models.BooleanField(default=True)
    remarks =  models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='delivery_man_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='delivery_man_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.name

class Courier(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='couriers')
    courier_service = models.ForeignKey(
        CourierService, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='couriers')
    delivery_man = models.ForeignKey(
        DeliveryMan, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='couriers')
    courier_status = models.CharField(max_length=30, choices=COURIER_STATUS, default="PENDING_PICKUP")
    slug = models.SlugField(max_length=255,unique=True)
    
    is_active = models.BooleanField(default=True)
    remarks =  models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='courier_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='courier_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return f"{self.order.invoice_no} and {self.courier_status}"
    
    
class CourierStatusLog(models.Model):
    courier = models.ForeignKey(
        Courier, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='courier_status_logs')
    slug = models.SlugField(max_length=255,unique=True)
    courier_status_code = models.CharField(max_length=50, blank=True, null=True)
    courier_status_display = models.CharField(max_length=50, blank=True, null=True)
    courier_status_change_reason = models.TextField(blank=True, null=True)
    status_change_by = models.JSONField(blank=True, null=True)
    status_change_at = models.DateTimeField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    remarks =  models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='courier_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='courier_status_log_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return f"{self.courier.order.invoice_no}"
    