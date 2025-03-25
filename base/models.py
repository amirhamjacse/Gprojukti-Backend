from django.db import models 
from user.models import UserAccount, UserInformation

# Create your models here.


DAYS = [
        ("SATURDAY", "Saturday"),
        ("SUNDAY", "Sunday"),
        ("MONDAY", "Monday"),
        ("TUESDAY", "Tuesday"),
        ("WEDNESDAY", "Wednesday"),
        ("THURSDAY", "Thursday"),
        ("FRIDAY", "Friday"),
    ]


PRODUCT_PRICE_TYPE = [
    ('ECOMMERCE', 'E-Commerce'),
    ('POINT_OF_SELL', 'Point of Sell'),
    ('CORPORATE', 'Corporate'),
    ('B2B', 'B2B'),
]

ORDER_TYPE = [
        ("ECOMMERCE_SELL", "E-Commerce Sell"),
        ("RETAIL_ECOMMERCE_SELL", "Retail E-Commerce Sell"),
        ("POINT_OF_SELL", "Point of Sell"),
        ("ON_THE_GO", "On the Go"),
        ("CORPORATE_SELL", "Corporate Sell"),
        ("B2B_SELL", "B2B Sell"),
        ("GIFT_ORDER", "Gift Order"),
        ("PC_BUILDER_SELL", "Pc Builder Order"),
        ("PRE_ORDER", "Pre-Order"),
        ("REPLACEMENT_ORDER", "Replacement Order"),
    ]

ADDRESS_TYPE = [
        ("HOME", "Home"),
        ("OFFICE", "Office"),
    ] 
   

PAYMENT_STATUS = [
        ("UNPAID", "Unpaid"),
        ("ADVANCE_PAID", "Advance Paid"),
        ("PARTIALLY_PAID", "Partially Paid"),
        ("EMI", "Emi"),
        ("PAID", "Paid"),
    ]

PAYMENT_TYPE = [
        ("CASH_ON_DELIVERY", "Cash On Delivery"),
        ("ONLINE_PAYMENT", "Online Payment"),
        ("PAY_AT_STORE", "Pay at Store"),
    ]

ORDER_APPROVED_STATUS = [
    ("INITIALIZED", "Initialized"),
    ("APPROVED", "Approved"),
    ("REJECTED", "Rejected"),
]

SERVICING_TYPE = [
    ("ORDER", "Order"),
    ("SERVICE", "Service"),
    ("OTHERS", "Others"),
]

ORDER_STATUS = [
        ('ORDER_RECEIVED', 'Order Received'),
        ('PRODUCT_AVAILABILITY_CHECK', 'Product Availability Check'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('PRODUCT_PURCHASED', 'Product Purchased'),
        ('PRELIMINARY_QC', 'Preliminary QC'),
        ('DETAILED_QC', 'Detailed QC'),
        ('PACKAGED', 'Packaged'),
        ('READY_FOR_PICKUP', 'Ready for Pickup'),
        ('IN_TRANSIT', 'In Transit'),
        ('DISPATCHED', 'Dispatched'),
        ('SHOP_DELIVERY_IN_TRANSIT', 'Shop Delivery in Transit'), 
        ('SHOP_RECEIVED', 'Shop Received'),
        ('DELIVERED_TO_CUSTOMER', 'Delivered To Customer'),
        ('DELIVERED', 'Delivered'), 
        ('CANCELLED', 'Cancelled'),
        ('RETURNED', 'Returned'),
        ('GSHEBA_RETURNED', 'G-Sheba Returned'),
        ('REFUNDED', 'Refunded'),
        
        # When The Order is Return
        ("SHOP_TO_WAREHOUSE", "Shop to Warehouse"),
        ("WAREHOUSE_RECEIVED", "Warehouse Received"),
        ("WAREHOUSE_TO_SERVICE_POINT", "Warehouse to Service Point"),
        ("SERVICE_POINT_RECEIVED", "Service Point Received"),
        ("WAREHOUSE_TO_VENDOR", "Warehouse to Vendor"),
        ("IN_SERVICING", "In Servicing"),
        ("SERVICE_POINT_TO_WAREHOUSE", "Service Point to Warehouse"),
        ("OTHERS", "Others"),
        
        # # This is for Only B2B, Corporate & Return
        # ("APPROVED", "Approved"),
        # ("REJECTED", "Rejected"),
    ]

ORDER_ITEM_STATUS = [
    ('ORDER_RECEIVED', 'Order Received'),
    ('PRODUCT_AVAILABILITY_CHECK', 'Product Availability Check'),
    ('ORDER_CONFIRMED', 'Order Confirmed'),
    ('PRODUCT_PURCHASED', 'Product Purchased'),
    ('PRELIMINARY_QC', 'Preliminary QC'),
    ('DETAILED_QC', 'Detailed QC'),
    ('PACKAGED', 'Packaged'),
    ('READY_FOR_PICKUP', 'Ready for Pickup'),
    ('IN_TRANSIT', 'In Transit'),
    ('DISPATCHED', 'Dispatched'),
    ('SHOP_DELIVERY_IN_TRANSIT', 'Shop Delivery in Transit'), 
    ('SHOP_RECEIVED', 'Shop Received'),
    ('DELIVERED_TO_CUSTOMER', 'Delivered To Customer'),
    ('DELIVERED', 'Delivered'), 
    ('CANCELLED', 'Cancelled'),
    ('RETURNED', 'Returned'),
    ('GSHEBA_RETURNED', 'G-Sheba Returned'),
    ('REFUNDED', 'Refunded'),
    
    # When The Order is Return
    ("SHOP_TO_WAREHOUSE", "Shop to Warehouse"),
    ("WAREHOUSE_RECEIVED", "Warehouse Received"),
    ("WAREHOUSE_TO_SERVICE_POINT", "Warehouse to Service Point"),
    ("SERVICE_POINT_RECEIVED", "Service Point Received"),
    ("WAREHOUSE_TO_VENDOR", "Warehouse to Vendor"),
    ("IN_SERVICING", "In Servicing"),
    ("SERVICE_POINT_TO_WAREHOUSE", "Service Point to Warehouse"),
    ("OTHERS", "Others"),
    ]

ORDER_PAYMENT_STATUS = [
    ('RECEIVED', 'Received'),
    ('REFUNDED', 'Refunded'),
]

ORDER_PAYMENT_TYPE = [
    ('PERSONAL', 'Personal'),
    ('AGENT', 'Agent'),
]

REQUISITION_STATUS = [
        ("INITIALIZED", 'Initialized'),
        ("APPROVED", 'Approved'),
        ("PARTIALLY_APPROVED", 'Partially Approved'),
        ("PURCHASED", 'Purchased'),
        ("IN_TRANSIT", 'In-Transit'),
        ("UPDATED", 'Updated'),
        ("FAILED", 'Failed'),
        ("ON_HOLD", 'On Hold'),
        ("CANCELLED", 'Cancelled'),
        ("DELIVERED", 'Delivered'),
    ] 

WARRANTY_DURATION=[
    ("DAY", "Day"),
    ("MONTH", "MONTH"),
    ("YEAR", "Year"),
    ("OTHERS", "Others"),
]
WARRANTY_TYPE = [
    ("1_GSHEBA_WARRANTY", "Gsheba"), # Priority 1
    ("2_COMPANY_WARRANTY", "Company Warranty"), # Priority  2
    ("3_REPLACEMENT_WARRANTY", "Replacement Warranty"), # Priority 3
    ("4_SERVICE_WARRANTY", "Service Warranty"), # Priority 4
    ("5_SUPPLIER_SERVICE_WARRANTY", "Supplier Warranty"), # Priority 5
]

COURIER_STATUS = [
    ("PENDING_PICKUP", "Pending Pickup"),
    ("IN_TRANSIT", "In Transit"),
    ("OUT_OF_DELIVERY", "Out of Delivery"),
    ("DELIVERED_TO_CUSTOMER", "Delivered to Customer"),
    ("DELAYED", "Delayed"),
    ("RETURNED", "Returned"),
    ("CANCELLED", "Cancelled"),
    ("PROBLEMATIC", "Problematic"),
    ("OTHERS", "Others"),
]
    

BARCODE_STATUS = [
    ("ACTIVE", "Active"), #
    ("FAULTY", "Faulty"),#
    ("DAMAGE", "Damage"),#
    ("IN_TRANSIT", "In-Transit"),
    ("IN_REQUISITION", "In-Requisition"),
    ("IN_TRANSFER", "In-Transfer"),
    ("RE_STOCK", "Re-Stock"),
    ("SOLD", "Sold"),
    ("DISCONTINUE", "Discontinue"),#
    ("RETURN", "Return"),
    ("REPLACEMENT", "Replacement"),
    ("BAD_LOSS", "Bad Loss"),
    ("CAN_BE_RESOLD", "Can Be Re-Sold"),
    ("NOT_SALABLE", "Not Salable"),
    ("GSHEBA_FAUlLY", "G-Sheba Faulty"),
    ("COMPANY_WARRANTY_FAUlLY", "Company Warranty Faulty"),
    ("PACKET_DAMAGE", "Packet Damage"),
    ("DEFECTIVE_ON_ARRIVAL", "Defective on Arrival"),
    ("REPLACEMENT_WARRANTY_FAULTY", "Replacement Warranty Faulty"),
    ("SERVICE_WARRANTY_FAULTY", "Service Warranty Faulty"),
    ("OTHERS", "Others"),
]

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('BASIC', 'Basic'),
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
    ]
    PLAN_TYPE = [
        ("LIFETIME", "Lifetime"),
        ("YEARS", "Years"),
        ("MONTH", "Month"),
        ("DAYS", "Days"),
    ]
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=255,unique=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default =  "FREE")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE, default =  "LIFETIME")
    plan_value = models.PositiveIntegerField(default = 0)
    
    category_limit = models.PositiveIntegerField(default=0)
    product_limit = models.PositiveIntegerField(default=0)
    employee_limit = models.PositiveIntegerField(default=0)
    shop_limit = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, 
        related_name='created_subscriptions')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, 
        related_name='updated_subscriptions',
        null=True, blank=True)
    
    def __str__(self):
        if self.plan:
            return self.plan
        else:
            return str(self.id)
        
class CompanyType(models.Model):
    name = models.CharField(max_length=255) # Marketplace, Service Center, Pharmacy
    slug = models.SlugField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='company_type_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='company_type_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
        
class PaymentType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    logo = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='payment_type_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='payment_type_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-id"]
        
        
class Company(models.Model):
    COMPANY_STATUS = [
        ("ACTIVE", "Active"),
        ("SUSPENDED", "Suspended"),
        ("INACTIVE", "Inactive"),
        ("OTHERS", "Others"),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    logo = models.TextField(null=True, blank=True)
    primary_phone = models.CharField(max_length=30)
    secondary_phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    website_url = models.URLField(max_length=255, null=True, blank=True)
    vat_registration_no = models.CharField(max_length=30, blank=True, null=True)
    registration_number = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
    starting_date = models.DateField(null=True,blank=True)
    company_owner = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='companys')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='companys')
    company_type = models.ForeignKey(CompanyType, on_delete=models.SET_NULL, null=True, blank=True, related_name='companys')
    payment_type = models.ManyToManyField(
        to=PaymentType,blank=True,
        related_name='companys'
        )
    currency = models.CharField(max_length=20, null=True, blank=True) # Ex: BDT, DOLLAR
    status = models.CharField(max_length=10, choices=COMPANY_STATUS, default='ACTIVE')
    remaining_days_subscription_ends = models.CharField(max_length=50, null=True, blank=True) # Auto Generate
    subscription_ends = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='company_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='company_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
        
    class Meta:
        ordering = ["name"]
    
    
class CompanySubscriptionLog(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, blank= True,
     related_name = 'company_subscription_logs')
    slug = models.SlugField(max_length=255,unique=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,null=True, blank= True,
     related_name = 'company_subscription_logs')
    end_date = models.DateTimeField(blank=True, null=True) # Auto generated
    
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='company_subscription_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='company_subscription_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.company:
            return str(self.company.name)
        else:
            return str(self.id)
    
    
class CompanyPaymentLog(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, blank= True,
     related_name = 'company_payment_logs')
    slug = models.SlugField(max_length=255,unique=True)
    payment_type =models.ManyToManyField(
        to=PaymentType,blank=True,
        related_name='company_payment_logs'
        )
    
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='company_payment_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='company_payment_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.company:
            return str(self.company.name)
        else:
            return str(self.id)
        
class CompanyHistory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, blank= True,
     related_name = 'company_history')
    slug = models.SlugField(max_length=255,unique=True)
    company_info = models.JSONField(null=True, blank=True)
    
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='company_history_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='company_history_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.company:
            return str(self.company.name)
        else:
            return str(self.id)
        
class TaxCategory(models.Model):
    TAX_TYPE = [
        ('SELL_TAX', "Sell Tax"),
        ('BUY_TAX', "Buy Tax")
    ]
    name =  models.CharField(max_length=150)
    slug = models.SlugField(max_length=255,unique=True)
    value_in_percentage = models.FloatField(default = 0.0)
    
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(blank=True, null=True)
    
    type = models.CharField(
        max_length=20, choices=TAX_TYPE,
        default='SELL_TAX'
        )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, blank= True,
     related_name = 'tax_categorys')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='tax_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='tax_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
    
    

class SMSMailSendLog(models.Model):
    SMS_TYPE = [
        ('SMS', "Sms"),
        ('EMAIL', "Email")
    ]
    SIM_TYPE = [
        ('GRAMEENPHONE', "Grameenphone"),
        ('ROBI', "Robi"),
        ('BANGLALINK', "Banglalink"),
        ('TELETALK', "Teletalk"),
        ('AIRTEL', "Airtel"),
        ('GMAIL', "G-Mail"),
    ]
    username =  models.CharField(max_length=150)
    subject = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=20, choices=SMS_TYPE,
        default='SMS'
        )
    sim_type = models.CharField(
        max_length=20, choices=SIM_TYPE,
        default='GRAMEENPHONE'
        )
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='sms_mail_send_log_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='sms_mail_send_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        if self.username:
            return self.username
        else:
            return str(self.id)
        
class UserNotification(models.Model):
    title = models.CharField(max_length=550) 
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default = True)
    remarks = models.TextField(null=True, blank=True)
    
    user_information = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='user_notifications',
        null=True, blank=True) # Notification For
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='user_notification_created_bys',
        null=True, blank=True)
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='user_notification_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.user_information:
            return self.user_information.email
        else:
            return str(self.title)