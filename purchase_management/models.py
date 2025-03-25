# models.py

from django.db import models
from django.utils import timezone
from user.models import UserAccount

class Specification(models.Model):
    key = models.CharField(max_length=50, unique=True)  

    def __str__(self):
        return self.key

class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    initiator = models.ForeignKey(UserAccount, related_name='initiated_purchases', on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='initiated')
    currently_assigned_to = models.ForeignKey(UserAccount, related_name='assigned_purchases', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Purchase {self.purchase_id}"

class Product(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    specification = models.JSONField(default=dict)  
    required_quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} in Purchase {self.purchase.purchase_id}"

class LogEntry(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='log_entries')
    date = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Purchase.STATUS_CHOICES)
    assigned_to = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_logentries_assigned_to'  
    )
    comment = models.TextField(null=True, blank=True)  
    created_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, related_name='purchase_logentries_created_by')

    def __str__(self):
        return f"{self.action} on Purchase {self.purchase.purchase_id} at {self.date}"

class Comment(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='comments', on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.date_time}"
    


class PurchaseData(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_data', on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    required_qty = models.PositiveIntegerField()
    vendor = models.CharField(max_length=100)
    previous_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2)
    required_budget = models.DecimalField(max_digits=12, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product} for Purchase {self.purchase.purchase_id}"
    

class PurchasePayment(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('card', 'Card'),
        ('bkash', 'Bkash'),
        ('rocket', 'Rocket'),
        ('nagad', 'Nagad'),
    )
    purchase = models.ForeignKey(Purchase, related_name='purchase_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_mode = models.CharField(max_length=16, choices=PAYMENT_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    paid_to = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, related_name='received_payments')
    paid_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, related_name='made_payments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Purchase {self.purchase.purchase_id}"
    

class StockModel(models.Model):
    store_name = models.CharField(max_length=100)
    pos_product_code = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()