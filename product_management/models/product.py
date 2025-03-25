from django.db import models
from user.models import UserAccount
from base.models import *
from django.utils.translation import gettext_lazy as _
from discount.models import Discount, PromoCode
from product_management.models.brand_seller import Brand, Seller, Supplier
from product_management.models.category import Category
from django.core.validators import MinValueValidator, MaxValueValidator
from location.models import OfficeLocation
from human_resource_management.models.employee import *


class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_attribute_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_attribute_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.SET_NULL, blank=True, null=True, related_name='product_attribute_values')
    name = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255)
    price = models.FloatField(default=0.0) 
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    # is_gift = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_attribute_value_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_attribute_value_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.value)
        
        
class Product(models.Model):
    STRUCTURECHOICES=[
        ("STANDALONE", "Stand Alone"),
        ("PARENT", "Parent"),
        ("CHILD", "Child"),
        ("CHILD_OF_CHILD", "Child of Child"),
    ]
    name =  models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    status = models.CharField(max_length=30, choices=STRUCTURECHOICES) # Auto Generated
    product_parent = models.ForeignKey('self',
                                on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='products',
                                help_text=_("Only choose a parent Category if you're creating a child "
                                "category.  For example if this is PC "
                                "3 of a particular [Normal, Gaming].  Leave blank if this is a "
                                "stand-alone Category (i.e. there is only one version of"
                                " this category).")
                    )
    gift_product = models.ForeignKey('self',
                                on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='gift_products')
    
    translation = models.JSONField(default=dict, blank=True, null=True ) 
    specifications = models.JSONField(default=dict, blank=True, null=True )
    meta = models.JSONField(default=dict, blank=True, null=True )
    
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    minimum_stock_quantity = models.IntegerField(default = 0)
    
    is_featured = models.BooleanField(default = True)
    is_top_sale = models.BooleanField(default = True)
    is_upcoming = models.BooleanField(default = True)
    is_new_arrival = models.BooleanField(default = True)
    is_on_the_go = models.BooleanField(default = True)
    is_out_of_stock = models.BooleanField(default = False)
    is_cart_disabled = models.BooleanField(default = False)
    is_gift_product = models.BooleanField(default=True)
    is_special_day = models.BooleanField(default = True)
    show_on_landing_page = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    is_commission_enable = models.BooleanField(default = True)
    remarks = models.TextField(blank=True, null=True)
    
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0) # Auto generate
    
    integrity_guaranteed = models.JSONField(default=dict, blank=True, null=True )
    product_code = models.CharField(max_length =350, null=True, blank=True)
    
    banner_message = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(
        to=Category,
        related_name='product_categorys'
        )
    sub_category = models.ManyToManyField(
        to=Category,blank=True,
        related_name='product_sub_categorys'
        )
    product_attribute_value = models.ManyToManyField(
        to=ProductAttributeValue,blank=True,
        related_name='products'
        )
    brand = models.ForeignKey(Brand,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='products')
    supplier = models.ForeignKey(Supplier,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='products')
    seller = models.ForeignKey(Seller,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='products')
    selling_tax_category = models.ForeignKey(TaxCategory,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='product_selling_tax_categorys')
    buying_tax_category = models.ForeignKey(TaxCategory,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='product_buying_tax_categorys')
    company = models.ForeignKey(Company,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='products') # Auto generate
    
    images = models.JSONField(default=list, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    serial_no = models.IntegerField(default=2500)
    
    """ For SEO Friendly for Operations """
    meta_title = models.CharField(max_length=200,null=True, blank=True)
    meta_image = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    og_title = models.CharField(max_length=200,null=True, blank=True)
    og_image = models.TextField(null=True, blank=True)
    og_url = models.TextField(null=True, blank=True)
    og_description = models.TextField(null=True, blank=True)
    canonical = models.URLField(null=True, blank=True)
    banner_image = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_updated_bys',
        null=True, blank=True)


    def __str__(self):
        return self.name
    

class ProductPriceInfo(models.Model):
    AMOUNT_TYPE = [
        ("PERCENTAGE", "Percentage"),
        ("FLAT", "Flat")
    ]
    
    product =  models.ForeignKey(Product,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='product_price_infos')
    discount = models.ForeignKey(Discount,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='product_price_infos')
    promo_code = models.ForeignKey(PromoCode,
                                on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='product_price_infos')
    product_price_type = models.CharField(max_length=350, 
                              choices=PRODUCT_PRICE_TYPE, default= "ECOMMERCE")
    buying_price = models.FloatField(default = 0.0)
    gsheba_amount = models.FloatField(default = 0.0)
    msp = models.FloatField(default = 0.0)  # Minimum Selling Price
    mrp = models.FloatField(default = 0.0) # Maximum Retail Price 
    # corporate_price = models.FloatField(default = 0.0) # Corporate Price 
    # b2b_price = models.FloatField(default = 0.0) # B2B Price 
    advance_amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE, default='FLAT')
    advance_amount = models.FloatField(default = 0.0) 
    
    
    is_active = models.BooleanField(default = True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_price_info_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_price_info_updated_bys',
        null=True, blank=True)
    
    
    def __str__(self):
        if self.product:
            return str(self.product.name)
        return str(self.id)
    

class ProductWarranty(models.Model):
    warranty_type = models.CharField(max_length=30, choices=WARRANTY_TYPE, default = "GSHEBA_WARRANTY")
    value = models.CharField(max_length=30)
    warranty_duration = models.CharField(max_length=50, choices=WARRANTY_DURATION, default = "MONTH")
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_warrantys'
        )
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_warranty_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_warranty_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    

class ProductStock(models.Model):
    barcode = models.CharField(max_length=50) # Like 32345-58374
    product_price_info = models.ForeignKey(
        ProductPriceInfo, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stocks'
        )
    status = models.CharField(max_length=50, choices=BARCODE_STATUS)
    stock_location =  models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stocks'
        )
    stock_in_date = models.DateTimeField(blank=True, null=True) # Status Wise Entry Date
    stock_in_age = models.CharField(max_length=350, blank=True, null=True) # Total Age Of Stock In
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.barcode
  
class ProductStockRequisition(models.Model):
    requisition_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=REQUISITION_STATUS, default="INITIALIZED")
    shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_requisitions'
        )
    total_need_quantity = models.FloatField(default = 0.0)
    total_approved_quantity = models.FloatField(default = 0.0)
    
    status_change_by =  models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_requisition_status_change_bys'
        )
    approved_by =  models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_requisition_approved_bys'
        ) # Who Can Change
    
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_requisition_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_requisition_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.requisition_no:
            return str(self.requisition_no)
        return f"{self.id}"  
    
class ProductStockRequisitionItem(models.Model):
    needed_quantity = models.FloatField(default = 0.0)
    status = models.CharField(max_length=20, choices=REQUISITION_STATUS, default="INITIALIZED")
    product_stock_requisition = models.ForeignKey(
        ProductStockRequisition, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_requisition_items'
        )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_requisition_items'
        )
    approved_quantity = models.FloatField(default = 0.0)
    
    status_change_by =  models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_requisition_item_status_change_bys'
        )
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_requisition_item_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_requisition_item_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.product_stock_requisition.requisition_no:
            return str(self.product_stock_requisition.requisition_no)
        return f"{self.id}"
    

class ProductStockRequisitionStatusLog(models.Model):
    product_stock_requisition = models.ForeignKey(
        ProductStockRequisition, on_delete=models.SET_NULL ,null=True, blank=True,related_name='product_stock_requisition_status_logs')
    status = models.CharField(max_length=250)
    status_display = models.CharField(max_length=250)
    order_status_reason = models.TextField(null=True, blank=True)
    status_changed_by = models.JSONField(blank=True, null=True)
    status_approved_by = models.JSONField(blank=True, null=True)
    status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_requisition_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_requisition_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.product_stock_requisition.requisition_no)
  

class ProductStockRequisitionItemStatusLog(models.Model):
    product_stock_requisition_item = models.ForeignKey(
        ProductStockRequisitionItem, on_delete=models.SET_NULL ,null=True, blank=True,related_name='product_stock_requisition_item_status_logs')
    status = models.CharField(max_length=250)
    status_display = models.CharField(max_length=250)
    order_status_reason = models.TextField(null=True, blank=True)
    status_changed_by = models.JSONField(blank=True, null=True)
    status_approved_by = models.JSONField(blank=True, null=True)
    status_change_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_requisition_item_status_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_requisition_item_status_log_updated_bys',
        null=True, blank=True)
    
    def __str__(self):
        return str(self.product_stock_requisition_item)
  
class ProductStockTransfer(models.Model):
    STOCK_TRANSFER_STATUS = [
        ("IN_TRANSIT", 'In-Transit'),
        ("NOT_UPDATED", 'Not Updated'),
        ("UPDATED", 'Updated'),
        ("APPROVED", 'Approved'),
        ("FAILED", 'Failed'),
        ("ON_HOLD", 'On Hold'),
        ("CANCELLED", 'Cancelled'),
    ]    
    STOCK_TRANSFER_TYPE = [
        ("TRANSFER", 'Transfer'),
        ("REQUISITION", 'Requisition'),
    ]
    requisition_no = models.CharField(max_length=50)
    product_requisition = models.ForeignKey(
        ProductStockRequisition, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_transfers'
        )
    status = models.CharField(max_length=20, choices=STOCK_TRANSFER_STATUS, default="IN_TRANSIT")
    stock_transfer_type = models.CharField(max_length=50, choices=STOCK_TRANSFER_TYPE, default="TRANSFER")
    product_stock = models.ManyToManyField(
        to=ProductStock,blank=True,
        related_name='product_stock_transfers'
        )
    from_shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='from_shop_product_stock_transfers'
        )
    to_shop = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='to_shop_product_stock_transfers'
        )
    mismatch_barcode_list = models.TextField(blank=True, null=True) # set Like ["12345-00001",  ]
    not_received_barcode_list = models.TextField(blank=True, null=True)
    received_barcode_list = models.TextField(blank=True, null=True)
    
    approved_by =  models.ForeignKey(
        EmployeeInformation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_transfers'
        )
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_transfer_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_transfer_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.requisition_no:
            return str(self.requisition_no)
        return f"{self.id}"
  
class ProductStockLog(models.Model):
    product_stock = models.ForeignKey(
        ProductStock, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_logs'
        )
    stock_location_info =  models.JSONField(null=True, blank=True)
    current_status = models.CharField(max_length=50)
    current_status_display = models.CharField(max_length=50)
    previous_status = models.CharField(max_length=50)
    previous_status_display = models.CharField(max_length=50)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stock_status_change_by_info =  models.JSONField(null=True, blank=True)
    
    stock_in_date = models.DateTimeField(blank=True, null=True) # Status Wise Entry Date
    stock_in_age = models.CharField(max_length=350, blank=True, null=True) # Total Age Of Stock In
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_log_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.product_stock:
            return self.product_stock.barcode
        return str(self.id)
    
class ProductStockTransferLog(models.Model):
    product_stock = models.ForeignKey(
        ProductStockTransfer, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_stock_transfer_logs'
        )
    from_shop_info =  models.JSONField(null=True, blank=True)
    to_shop_info =  models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=50)
    status_display = models.CharField(max_length=50)
    stock_transfer_type = models.CharField(max_length=50)
    stock_transfer_type_display = models.CharField(max_length=50)
    
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stock_status_change_by_info =  models.JSONField(null=True, blank=True)
    
    status_changed_date = models.DateTimeField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_stock_transfer_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_stock_transfer_log_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.status
  
class ProductLog(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='product_logs'
        )
    product_info =  models.JSONField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='product_logs_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='product_logs_updated_bys',
        null=True, blank=True)

    def __str__(self):
        return self.status
  
class ShopWiseZeroStockLog(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='shop_wise_zero_stock_logs'
        )
    office_location = models.ForeignKey(
        OfficeLocation, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='shop_wise_zero_stock_logs'
        )
    zero_stock_date = models.DateTimeField(null=True, blank=True)
    
    remarks = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE ,related_name='shop_wise_zero_stock_log_created_bys')
    updated_by = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE,  related_name='shop_wise_zero_stock_log_updated_bys',
        null=True, blank=True)

    def __str__(self):
        if self.product:
            return self.product.name
        elif self.office_location:
            return self.office_location.name
        return f"{self.id}"
    
    
    
    