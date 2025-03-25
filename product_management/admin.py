from django.contrib import admin
from product_management.models.brand_seller import *
from product_management.models.category import *
from product_management.models.product import *

# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name',"slug", "created_at"]

    class Meta:
        model = Brand
admin.site.register(Brand, BrandAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id','name',"slug", "created_at"]

    class Meta:
        model = Supplier
admin.site.register(Supplier, SupplierAdmin)

class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ['id','name','company', 'slug','banner_image',"created_at"]

    class Meta:
        model = CategoryGroup
admin.site.register(CategoryGroup, CategoryGroupAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug', 'status', 'category_group', 'category_parent', 'is_for_pc_builder',"created_at"]

    class Meta:
        model = Category
admin.site.register(Category, CategoryAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id','name', "created_at"]

    class Meta:
        model = ProductAttribute
admin.site.register(ProductAttribute, ProductAttributeAdmin)


class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id','product_attribute','slug','value' ,"created_at"]

    class Meta:
        model = ProductAttributeValue
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','id','status','slug', 'company', 'sku','product_code', 'brand', 'supplier', "created_at"]
    search_fields = ['name', 'product_code']
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)

class ProductPriceInfoAdmin(admin.ModelAdmin):
    list_display = ['id','product','discount', 'promo_code','product_price_type', 'msp', 'mrp','advance_amount', "created_at"]

    class Meta:
        model = ProductPriceInfo
admin.site.register(ProductPriceInfo, ProductPriceInfoAdmin)

class ProductWarrantyAdmin(admin.ModelAdmin):
    list_display = ['id','warranty_type', 'value', 'product',"created_at"]

    class Meta:
        model = ProductWarranty
admin.site.register(ProductWarranty, ProductWarrantyAdmin)

class ProductStockAdmin(admin.ModelAdmin):
    list_display = ['id','barcode','product_price_info' ,'status', 'stock_location','stock_in_age', "created_at"]
    list_filter = ['stock_location__name', "status"]

    search_fields = ['barcode']
    class Meta:
        model = ProductStock
admin.site.register(ProductStock, ProductStockAdmin)

class ProductStockLogAdmin(admin.ModelAdmin):
    list_display = ['id','product_stock', 'stock_in_date','stock_in_age','current_status', "created_at"]

    class Meta:
        model = ProductStockLog
admin.site.register(ProductStockLog, ProductStockLogAdmin)

class ProductLogAdmin(admin.ModelAdmin):
    list_display = ['id','product', "created_at"]

    class Meta:
        model = ProductLog
admin.site.register(ProductLog, ProductLogAdmin)

class SellerAdmin(admin.ModelAdmin):
    list_display = ['id','name','code', "created_at"]

    class Meta:
        model = Seller
admin.site.register(Seller, SellerAdmin)

class ProductStockTransferAdmin(admin.ModelAdmin):
    list_display = ['id','requisition_no' ,'status','from_shop', 'to_shop', 'approved_by',"created_at"]

    class Meta:
        model = ProductStockTransfer
admin.site.register(ProductStockTransfer, ProductStockTransferAdmin)



class ProductStockTransferLogAdmin(admin.ModelAdmin):
    list_display = ['id','product_stock','status_display', "created_at"]

    class Meta:
        model = ProductStockTransferLog
admin.site.register(ProductStockTransferLog, ProductStockTransferLogAdmin)


class ProductStockRequisitionAdmin(admin.ModelAdmin):
    list_display = ['id','requisition_no','status','total_need_quantity', "created_at"]

    class Meta:
        model = ProductStockRequisition
admin.site.register(ProductStockRequisition, ProductStockRequisitionAdmin)

class ProductStockRequisitionStatusLogAdmin(admin.ModelAdmin):
    list_display = ['id','product_stock_requisition','status', "created_at"]

    class Meta:
        model = ProductStockRequisitionStatusLog
admin.site.register(ProductStockRequisitionStatusLog, ProductStockRequisitionStatusLogAdmin)

class ProductStockRequisitionItemAdmin(admin.ModelAdmin):
    list_display = ['id','product_stock_requisition','status', "created_at"]

    class Meta:
        model = ProductStockRequisitionItem
admin.site.register(ProductStockRequisitionItem, ProductStockRequisitionItemAdmin)

class ProductStockRequisitionItemStatusLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'status',"created_at"]

    class Meta:
        model = ProductStockRequisitionItemStatusLog
admin.site.register(ProductStockRequisitionItemStatusLog, ProductStockRequisitionItemStatusLogAdmin)

class ShopWiseZeroStockLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'office_location', 'zero_stock_date', 'remarks',"created_at"]

    class Meta:
        model = ShopWiseZeroStockLog
admin.site.register(ShopWiseZeroStockLog, ShopWiseZeroStockLogAdmin)
