from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer, EmployeeInformationBaseSerializer, TaxCategorySerializer
from discount.serializers import DiscountListSerializer, PromoCodeListSerializer
from gporjukti_backend_v2.settings import BASE_URL
from human_resource_management.serializers.employee import EmployeeInformationLiteSerializer
from location.serializers import OfficeLocationListSerializer, OfficeLocationLiteSerializer
from order.models import ProductReview
from product_management.models.product import *
from product_management.serializers.brand_seller import *
from product_management.serializers.category import CategoryLiteSerializer
from user.serializers import BaseSerializer
from drf_extra_fields.fields import Base64FileField, Base64ImageField

from django.db.models import Q

from utils.base import *
from utils.calculate import offer_check
import random

from utils.constants import *
from utils.upload_image import image_upload

import aiohttp
import asyncio
from django.utils import timezone
from datetime import datetime
from django.db.models import Count


class ProductVariantListSerializer(serializers.ModelSerializer):
    price_details = serializers.SerializerMethodField(read_only = True)
    images = serializers.SerializerMethodField(read_only = True)
    product_attribute_value = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'images',
            'price_details',
            'product_attribute_value',
        ]
        
    def get_images(self, obj):
        image_url = product_image(product = obj)
        return image_url
    
    def get_price_details(self, obj):
        product_price = product_price_details(product = obj, product_price_type='ECOMMERCE')
            
        return product_price
    
    def get_product_attribute_value(self, obj):
        product_attribute_value = []
        
        if obj.product_attribute_value:
            
            product_attribute_qs = ProductAttribute.objects.filter(
                name__in = obj.product_attribute_value.all().values_list('product_attribute__name', flat=True)
            )
            
            product = obj
            product_attribute_list = product_attribute_qs
            
            product_attribute_value = product_attribute_value_list(product, product_attribute_list)
            
        return product_attribute_value
            
class ProductLiteSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
        ]
    
    def get_image(self, obj):
        image_url = product_image(product = obj)
        return image_url
            
    
class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    price_details = serializers.SerializerMethodField(read_only = True) 
    total_stock = serializers.SerializerMethodField(read_only = True)
    brand = serializers.SerializerMethodField(read_only = True)
    supplier = serializers.SerializerMethodField(read_only = True)
    is_out_of_stock = serializers.SerializerMethodField(read_only = True)
    is_child = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'product_code',
            'sku',
            'brand',
            'supplier',
            'total_stock',
            'price_details',
            'is_out_of_stock',
            'is_child',
        ]
        
    def get_image(self, obj):
        image_url = product_image(product = obj)
        return image_url
    
    def get_is_child(self, obj):
        is_child = False
        
        qs = Product.objects.filter(product_parent__slug = obj.slug)
        print('ffffffffff', obj.product_parent)
        if obj.product_parent:
            is_child = True
        
        return is_child
    
    def get_brand(self, obj):
        id = None
        name = None
        slug = None
        
        if obj.brand:
            id = obj.brand.id
            name = obj.brand.name
            slug = obj.brand.slug
        
        context = {
            'id':id,
            'name':name,
            'slug':slug,
            
        }
        return context
    
    def get_supplier(self, obj):
        id = None
        name = None
        slug = None
        
        if obj.supplier:
            id = obj.supplier.id
            name = obj.supplier.name
            slug = obj.supplier.slug
        
        context = {
            'id':id,
            'name':name,
            'slug':slug,
            
        }
        return context
    
    
    def get_total_stock(self, obj):
        total_stock = 0
        product_stock_qs = ProductStock.objects.filter(
            product_price_info__product = obj
        )
        
        total_stock = product_stock_qs.count()
        
        return total_stock
    
    
    def get_price_details(self, obj):
        product_price = product_price_details(product = obj, product_price_type='ECOMMERCE')
            
        return product_price
    
    def get_is_out_of_stock(self, obj):
        is_out_of_stock = False
        
        product_price = product_price_details(product = obj, product_price_type='ECOMMERCE')
        mrp = product_price.get('mrp') or 0
        
        if mrp < 1:
            is_out_of_stock = True
            
        return is_out_of_stock
    
    
class ShopProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    price_details = serializers.SerializerMethodField(read_only=True)
    warranty_details = serializers.SerializerMethodField(read_only=True)
    total_stock = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'product_code',
            'total_stock',
            'price_details',
            'is_out_of_stock',
            'warranty_details',
        ]
        
    def get_name(self, obj):
        name = obj.name
        
        product_price = obj.product_price_infos.filter(product_price_type='POINT_OF_SELL').last()
        
        if product_price:
            promo_code_qs = product_price.promo_code
            
            if promo_code_qs:
                discount = offer_check(promo_code_qs)
                discount_status = discount.get('valid_status')
                
                if discount_status == 'Active':
                    name = f"{name} (Promo Code = {promo_code_qs.promo_code})"
            
        return name
    
        
    def get_image(self, obj):
        image_url = product_image(product=obj)
        return image_url
    
    def get_warranty_details(self, obj):
        if obj.product_warrantys.exists():
            serializer = ProductWarrantyListSerializer(obj.product_warrantys.order_by('warranty_type'), many=True)
            return serializer.data
        return None
    
    def get_price_details(self, obj):
        product_price = product_price_details(
            product=obj, 
            product_price_type='POINT_OF_SELL')
        return product_price

    def get_total_stock(self, obj):
        total_stock = 0
        try:
        
            user = self.context['request'].user
            
            shop_qs = get_user_store_list(user)
            
            product_stock_qs = ProductStock.objects.exclude(status__in = ['IN_TRANSIT', 'IN_REQUISITION', 'IN_TRANSFER', 'SOLD']).filter(
                product_price_info__product__slug = obj.slug,
                stock_location__slug__in = shop_qs.values_list('slug', flat = True)
            )
            
            # print(f"Status = {product_stock_qs.values_list('status', flat=True).distinct()}")
            status_count_qs = product_stock_qs.values('status').annotate(count=Count('status'))

            # Print the distinct statuses and their counts
            status_msg = []
            for status_count in status_count_qs:
                status_msg.append((f"Status: {status_count['status']}, Count: {status_count['count']}"))
            
            total_stock = f"Total {product_stock_qs.count()}"
            # total_stock = f"Total {product_stock_qs.count()} and {status_msg}"
            
        except:
            pass
        
        return total_stock


class ShopProductListBarcodeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    price_details = serializers.SerializerMethodField(read_only=True)
    warranty_details = serializers.SerializerMethodField(read_only=True)
    total_stock = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    product_stocks = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'product_code',
            'total_stock',
            'price_details',
            'is_out_of_stock',
            'warranty_details',
            'product_stocks',
        ]
        
    def get_name(self, obj):
        name = obj.name
        
        product_price = obj.product_price_infos.filter(product_price_type='POINT_OF_SELL').last()
        
        if product_price:
            promo_code_qs = product_price.promo_code
            
            if promo_code_qs:
                discount = offer_check(promo_code_qs)
                discount_status = discount.get('valid_status')
                
                if discount_status == 'Active':
                    name = f"{name} (Promo Code = {promo_code_qs.promo_code})"
            
        return name

    def get_product_stocks(self, obj):
        product_stocks = ProductStock.objects.filter(
            product_price_info__product=obj
        )
        return [
            {
                'barcode': stock.barcode,
                'status': stock.status,
            }
            for stock in product_stocks
        ]

    def get_image(self, obj):
        image_url = product_image(product=obj)
        return image_url
    
    def get_warranty_details(self, obj):
        if obj.product_warrantys.exists():
            serializer = ProductWarrantyListSerializer(obj.product_warrantys.order_by('warranty_type'), many=True)
            return serializer.data
        return None
    
    def get_price_details(self, obj):
        product_price = product_price_details(
            product=obj, 
            product_price_type='POINT_OF_SELL')
        return product_price

    def get_total_stock(self, obj):
        total_stock = 0
        try:
        
            user = self.context['request'].user
            
            shop_qs = get_user_store_list(user)
            
            product_stock_qs = ProductStock.objects.exclude(status__in = ['IN_TRANSIT', 'IN_REQUISITION', 'IN_TRANSFER', 'SOLD']).filter(
                product_price_info__product__slug = obj.slug,
                stock_location__slug__in = shop_qs.values_list('slug', flat = True)
            )
            
            # print(f"Status = {product_stock_qs.values_list('status', flat=True).distinct()}")
            status_count_qs = product_stock_qs.values('status').annotate(count=Count('status'))

            # Print the distinct statuses and their counts
            status_msg = []
            for status_count in status_count_qs:
                status_msg.append((f"Status: {status_count['status']}, Count: {status_count['count']}"))
            
            total_stock = f"Total {product_stock_qs.count()}"
            # total_stock = f"Total {product_stock_qs.count()} and {status_msg}"
            
        except:
            pass
        
        return total_stock



class ProductStockSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields=[
            'id',
            'barcode',
            'status',
            'is_active',
            'stock_in_date',
            'stock_in_age'

        ]


class ShopProductListSerializerShop(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    price_details = serializers.SerializerMethodField(read_only=True)
    warranty_details = serializers.SerializerMethodField(read_only=True)
    total_stock = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    barcode_list = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'product_code',
            'total_stock',
            'price_details',
            'is_out_of_stock',
            'warranty_details',
            'barcode_list',
        ]
        
    def get_name(self, obj):
        name = obj.name
        
        product_price = obj.product_price_infos.filter(product_price_type='POINT_OF_SELL').last()
        
        if product_price:
            promo_code_qs = product_price.promo_code
            
            if promo_code_qs:
                discount = offer_check(promo_code_qs)
                discount_status = discount.get('valid_status')
                
                if discount_status == 'Active':
                    name = f"{name} (Promo Code = {promo_code_qs.promo_code})"
            
        return name
    
        
    def get_image(self, obj):
        image_url = product_image(product=obj)
        return image_url
    
    def get_warranty_details(self, obj):
        if obj.product_warrantys.exists():
            serializer = ProductWarrantyListSerializer(obj.product_warrantys.order_by('warranty_type'), many=True)
            return serializer.data
        return None
    
    def get_price_details(self, obj):
        product_price = product_price_details(
            product=obj, 
            product_price_type='POINT_OF_SELL')
        return product_price

    def get_total_stock(self, obj):
        total_stock = 0
        try:
        
            user = self.context['request'].user
            
            print('fffffffffff', user)
            
            shop_qs = get_user_store_list(user)
            
            pr_qs= ProductStock.objects.filter(
                product_price_info__product__slug = obj.slug,
                stock_location__slug__in = shop_qs.values_list('slug', flat = True)
            )
            product_stock_qs = pr_qs.filter(status="ACTIVE")
            
            # print(f"Status = {product_stock_qs.values_list('status', flat=True).distinct()}")
            status_count_qs = product_stock_qs.values('status').annotate(count=Count('status'))

            # Print the distinct statuses and their counts
            status_msg = []
            for status_count in status_count_qs:
                status_msg.append((f"Status: {status_count['status']}, Count: {status_count['count']}"))
            
            total_stock = f"Total {product_stock_qs.count()} and {status_msg}"
            
        except:
            pass
        
        return total_stock


    def get_barcode_list(self,obj):
            user = self.context['request'].user
            shop_qs = get_user_store_list(user)

            product_stock_qs = ProductStock.objects.filter(
                status="ACTIVE",
                product_price_info__product__slug = obj.slug,
                stock_location__slug__in = shop_qs.values_list('slug', flat = True)
            )

            return ProductStockSerializerLite(product_stock_qs, many=True).data


class ProductAttributeValueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = [
            'id',
            'value',
            'price',
            'slug',
        ]    
class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_value = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = ProductAttribute
        fields = [
            'id',
            'name',
            "slug",
            "attribute_value",
                ]
        
    def get_attribute_value(self, obj):
        if obj.product_attribute_values:
            serializer = ProductAttributeValueListSerializer(instance=obj.product_attribute_values, many = True)
            return serializer.data
        return None
        
    

class Base64ImageListFieldSerializer(serializers.Serializer):
    image = Base64ImageField(write_only=True)

class ProductBulkCreateSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True)
    
class ProductCreateSerializer(serializers.ModelSerializer): 
    product_parent = serializers.CharField(required=False) 
    brand = serializers.CharField(required=False) 
    supplier = serializers.CharField(required=False) 
    seller = serializers.CharField(required=False) 
    selling_tax_category = serializers.CharField(required=False) 
    buying_tax_category = serializers.CharField(required=False) 
    gift_product = serializers.CharField(required=False) 
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'images',
            'product_parent',
            'category',
            'sub_category',
            'brand',
            'supplier',
            'seller',
            'selling_tax_category',
            'buying_tax_category',
            'translation',
            'minimum_stock_quantity',
            'product_code',
            'sku',
            'video_link',
            'is_featured',
            'is_upcoming',
            'is_new_arrival',
            'is_on_the_go',
            'is_special_day',
            'is_gift_product',
            'show_on_landing_page',
            'gift_product',
            'is_commission_enable',
            'is_active',
            'remarks',
            'product_attribute_value',
            'specifications',
                  ] 
    
class ProductUpdateSerializer(serializers.ModelSerializer):
    # images_file = Base64ImageListFieldSerializer(required=False, many=True)   
    product_parent = serializers.CharField(required=False) 
    brand = serializers.CharField(required=False) 
    supplier = serializers.CharField(required=False) 
    seller = serializers.CharField(required=False) 
    selling_tax_category = serializers.CharField(required=False) 
    buying_tax_category = serializers.CharField(required=False) 
    gift_product = serializers.CharField(required=False) 
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'images',
            'product_parent',
            'category',
            'sub_category',
            'brand',
            'supplier',
            'seller',
            'selling_tax_category',
            'buying_tax_category',
            'translation',
            'minimum_stock_quantity',
            'video_link',
            'is_featured',
            'is_upcoming',
            'is_new_arrival',
            'is_new_arrival',
            'is_out_of_stock',
            'is_gift_product',
            'is_top_sale',
            'is_cart_disabled',
            'is_on_the_go',
            'is_special_day',
            'show_on_landing_page',
            'gift_product',
            'is_commission_enable',
            'is_active',
            'remarks',
            'product_attribute_value',
            'specifications',
                  ] 
   
class ProductPriceInfoCreateSerializer(serializers.ModelSerializer):
    discount = serializers.CharField(required = False)
    promo_code = serializers.CharField(required = False)
    
    class Meta:
        model = ProductPriceInfo
        fields = [
            'id',
            'discount',
            'promo_code',
            'product_price_type',
            'advance_amount_type',
            'buying_price',
            'gsheba_amount',
            'msp',
            'mrp',
            'advance_amount',
            ]
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["product"] = ProductListSerializer(read_only=True)
        return super(ProductPriceInfoCreateSerializer, self).to_representation(instance)
    
    
class ProductDescriptionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'id',
            'description',
            'meta_title',
            'meta_image',
            'meta_description',
            'og_title',
            'og_image',
            'og_url',
            'short_description',
            'og_description',
            'canonical',
            'translation',
            'integrity_guaranteed',
                  ]
        
class ProductWarrantyCreateSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ProductWarranty
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["product"] = ProductListSerializer(read_only=True)
        return super(ProductWarrantyCreateSerializer, self).to_representation(instance)
        
        
class ProductWarrantySerializer(serializers.ModelSerializer):
    warranty_type_display = serializers.CharField(source='get_warranty_type_display')
    class Meta:
        model = ProductWarranty
        fields = '__all__'
        
class ProductWarrantyListSerializer(serializers.ModelSerializer):
    warranty_type_display = serializers.CharField(source='get_warranty_type_display')
    class Meta:
        model = ProductWarranty
        fields = [
                'id',  
                'warranty_type',  
                'warranty_duration',  
                'value',  
                'warranty_type_display',  
                ]
        
class ProductAttributeValueCreateUpdateSerializer(serializers.ModelSerializer):  
    product_attribute = serializers.CharField()
    class Meta:
        model = ProductAttributeValue
        fields = [
            'product_attribute',
            'value',
                ]

class ProductPriceInfoSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField(read_only =True)
    product_price_type_display = serializers.CharField(source='get_product_price_type_display')
    class Meta:
        model = ProductPriceInfo
        fields = "__all__"
        
    def to_representation(self, instance):
        self.fields["discount"] = DiscountListSerializer(read_only=True)
        self.fields["promo_code"] = PromoCodeListSerializer(read_only=True)
        return super(ProductPriceInfoSerializer, self).to_representation(instance)
        
    def get_product_info(self, obj):
        context = {}
        
        if obj.product:
            if obj.product.images:
                image_url = obj.product.images[0]
            else:
                image_url = f"{BASE_URL}/assets/images/no-image-available.jpg"
                
            context = {
                'id': obj.product.id,
                'name': obj.product.name,
                'slug': obj.product.slug,
                'image': image_url,
            } 
        return context
        
class ProductDetailsSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    company = CompanyLiteSerializer(read_only=True)
    category = CategoryLiteSerializer(read_only=True, many=True)
    sub_category = CategoryLiteSerializer(read_only=True, many=True)
    # images = serializers.FileField(write_only=True, required=False)
    product_price_details = serializers.SerializerMethodField(read_only = True)
    product_attribute_value = serializers.SerializerMethodField(read_only = True)
    review_ratting_details = serializers.SerializerMethodField(read_only = True)
    product_warranty_details = serializers.SerializerMethodField(read_only = True)
    total_order = serializers.SerializerMethodField(read_only = True)
    product_variant = serializers.SerializerMethodField(read_only = True)
    breadcrumb = serializers.SerializerMethodField(read_only = True)
    # short_description = serializers.SerializerMethodField(read_only = True)
    # description = serializers.SerializerMethodField(read_only = True)
    images = serializers.SerializerMethodField(read_only = True)
    # integrity_guaranteed = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Product
        fields = "__all__"
       
    def to_representation(self, instance):
        self.fields["product_parent"] = ProductListSerializer(read_only=True)
        self.fields["gift_product"] = ProductListSerializer(read_only=True)
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["seller"] = SellerSerializer(read_only=True)
        self.fields["brand"] = BrandListSerializer(read_only=True)
        self.fields["supplier"] = SupplierSerializer(read_only=True)
        self.fields["selling_tax_category"] = TaxCategorySerializer(read_only=True)
        self.fields["buying_tax_category"] = TaxCategorySerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        self.fields["category"] = CategoryLiteSerializer(read_only=True, many=True)
        self.fields["sub_category"] = CategoryLiteSerializer(read_only=True, many=True)
        # self.fields["product_attribute_value"] = ProductAttributeValueListSerializer(read_only=True, many=True)
        return super(ProductDetailsSerializer, self).to_representation(instance)
    
    def get_product_warranty_details(self, obj):
        if obj.product_warrantys:
            serializer = ProductWarrantySerializer(instance = obj.product_warrantys, many = True)
            return serializer.data
        return None
    
    # def get_integrity_guaranteed(self, obj):
    #     if obj:
    #         context = {
    #             "quality": "yellow",
    #             "authenticity": "yellow", 
    #             "seller_reliability": "green"
    #             }
            
    #     return context
    
    # def get_short_description(self, obj):
    #     short_description = f"<p>HP EliteBook 840 G3 Ci5 Touch<br />Intel Core i5-6200U (2.3 GHz )<br />ডিসপ্লে 14.1&Prime;&nbsp;<br />8 GB DDR4-2400 SDRAM<br />256 GB M.2 SATA SSD<br />Intel &reg; UHD গ্রাফিক্স 520</p> <br> <br> <p>HP EliteBook 840 G3 Ci5 Touch<br />Intel Core i5-6200U (2.3 GHz )<br />ডিসপ্লে 14.1&Prime;&nbsp;<br />8 GB DDR4-2400 SDRAM<br />256 GB M.2 SATA SSD<br />Intel &reg; UHD গ্রাফিক্স 520</p> <br><br><p>HP EliteBook 840 G3 Ci5 Touch<br />Intel Core i5-6200U (2.3 GHz )<br />ডিসপ্লে 14.1&Prime;&nbsp;<br />8 GB DDR4-2400 SDRAM<br />256 GB M.2 SATA SSD<br />Intel &reg; UHD গ্রাফিক্স 520</p> <br> <br> <p>HP EliteBook 840 G3 Ci5 Touch<br />Intel Core i5-6200U (2.3 GHz )<br />ডিসপ্লে 14.1&Prime;&nbsp;<br />8 GB DDR4-2400 SDRAM<br />256 GB M.2 SATA SSD<br />Intel &reg; UHD গ্রাফিক্স 520</p>"
        
    #     return short_description

    # def get_description(self, obj):
    #     description = "<p><strong>Model:</strong> Vostro 14 3400<br /><strong>Processor:</strong> Intel Core i7-1165G7 Processor (12MB Cache, 2.80 GHz up to 4.70 GHz)<br /><strong>Display:</strong> 14.0-inch FHD (1920 x 1080) Anti-glare LED Backlight Non-touch Narrow Border WVA Display<br /><strong>Memory:</strong> 8GB, 1x8GB, DDR4 RAM<br /><strong>Storage:</strong> 512GB M.2 PCIe NVMe Solid State Drive<br /><strong>Graphics:</strong> NVIDIA GeForce MX350 with 2GB GDDR5 graphics memory<br /><strong>Operating System:</strong> Free DOS<br /><strong>Battery:</strong> 3-Cell Battery, 40WHr (Integrated)<br /><strong>Adapter:</strong> 45 Watt AC Adaptor<br /><strong>Keyboard:</strong> Dark Grey Keyboard Non-Backlit<br /><strong>WebCam:</strong> 1280x720 Intergrated HD Webcam<br /><strong>Card Reader:</strong> 1x 3-in-1 SD Media Card Reader<br /><strong>Wi-Fi:</strong> 802.11ac 2x2 WiFi<br /><strong>Bluetooth:</strong> Yes<br /><strong>USB (s):</strong> 1x USB 3.2 Gen 1 Type-C (Data only)<br />2x USB 3.2 Gen 1 Type-A<br /><strong>HDMI:</strong> 1x HDMI 1.4b<br /><strong>Audio Jack Combo:</strong> 3.5 mm Headset Jack<br /><strong>Dimensions (W x D x H):</strong> Height: Front: 0.66 '(16.74 mm) Rear: 0.7 (17.9 mm)<br />Width: 12.65 (321.3 mm)<br />Depth: 8.51 (216.2 mm)<br /><strong>Weight:</strong> 3.03 lb (1.36 kg)<br /><strong>Color(s):</strong> Black</p>"
        
    #     return description
    
    def get_breadcrumb(self, obj):
        sub_category_name = 'Sub-Category/Name/'
        sub_category_slug = 'Sub-Category/Sug/'
        sub_category_path = 'Sub-Category/Path/' 
        
        product_group_name = 'Product-Group/Name/'
        product_group_slug = 'Product-Group/Sug/'
        product_group_path = 'Product-Group/Path/'
        
        category_name = 'Category/Name/'
        category_slug = 'Category/Sug/'
        category_path = 'Category/Path/'
        
        product_name = 'Category/Name/'
        product_slug = 'Category/Sug/'
        product_path = 'Product/Path/'
        
        if obj.sub_category:
            try:
                sub_category_name = obj.sub_category.last().name
                sub_category_slug = obj.sub_category.last().slug
                sub_category_path = f"/product-category/{obj.category.last().category_group.slug}/{obj.category.last().slug}/{obj.sub_category.last().slug}"
            except:
                pass
        
        try:
            
            if obj.category: 
                category_name = obj.category.last().name
                category_slug = obj.category.last().slug
                category_path = f"/product-category/{obj.category.last().category_group.slug}/{obj.category.last().slug}"
        except:
            pass
        
            
        try:
            if obj.category.last().category_group:
            
                product_group_name = obj.category.last().category_group.name
                product_group_slug = obj.category.last().category_group.slug
                product_group_path = f"/product-category/{obj.category.last().category_group.slug}"
        except:
            pass
        
        try:
            if obj:
            
                product_name = obj.name
                product_slug = obj.slug
                product_path = f"/product-category/{obj.category.last().category_group.slug}/{obj.category.last().slug}/{obj.sub_category.last().slug}/{obj.slug}"
        except:
            pass
            
        data_list = [
            {
                'name':"Home",
                'slug':"/",
                'path':"/",
            },
            {
                'name':product_group_name,
                'slug':product_group_slug,
                'path':product_group_path,
            },
            {
                'name': category_name,
                'slug': category_slug,
                'path': category_path,
                 
            },
            {
                'name':sub_category_name,
                'slug':sub_category_slug,
                'path':sub_category_path,
            },
            {
                'name':product_name,
                'slug':product_slug,
                'path':product_path,
            },
        ]
        
        
        return data_list
    
    
    def get_product_attribute_value(self, obj):
        product_attribute_value = []
        
        if obj.product_attribute_value:
            product_variant_qs = Product.objects.filter(product_parent__slug = obj.slug)
            
            product_attribute_qs = ProductAttribute.objects.filter(
                Q(name__in = obj.product_attribute_value.all().values_list('product_attribute__name', flat=True))
                | Q(name__in = product_variant_qs.values_list('product_attribute_value__product_attribute__name', flat=True))
            )
            
            product = obj
            product_attribute_list = product_attribute_qs
            
            product_attribute_value = parent_product_attribute_value_list(product, product_attribute_list)
            
        return product_attribute_value
    
    def get_product_variant(self, obj):
        product_variant_qs = Product.objects.filter(product_parent__slug = obj.slug)
        
        if product_variant_qs:
            serializer = ProductVariantListSerializer(instance=product_variant_qs, many = True)
            return serializer.data
        return None
    
    def get_product_price_details(self, obj):
        if obj.product_price_infos.all():
            serializer = ProductPriceInfoSerializer(instance = obj.product_price_infos, many = True)
            return serializer.data
        return None
    
    def get_review_ratting_details(self, obj):
        context = {}
        total_customer_review = 4320
        all_rating = {}
        total_rating = 0
        review_list = []
        
        
        all_rating = {
            # 'five_star': 1044,
            # 'four_star': 34,
            # 'three_star': 534,
            # 'two_star': 1254,
            # 'one_star': 1534,
        }
        # review_list.append({
        #     'review_by': 'admin@gmail.com',
        #     'message': 'Superb sweatshirt. I loved it. It is for winter.',
        #     'review_at': 'Jan 08 at 02:46 pm'
        # })

        # review_list.append({
        #     'review_by': 'remon@gmail.com',
        #     'message': 'Great at this price, Product quality and look are awesome.',
        #     'review_at': 'Jan 08 at 02:46 pm'
        # })
        
        context = {
            'total_customer_review':total_customer_review,
            'total_rating':total_rating,
            'all_rating':all_rating,
            'review_list':review_list,
        }
        
        return context
    
    def get_total_order(self, obj):
        total_order = 0
        
        return total_order
    
    # def get_images(self, obj):
    #     image_list = [
    #         # settings.NOT_FOUND_IMAGE,
    #         # settings.NOT_FOUND_IMAGE
    #             ] 
        
    #     product_variant_qs = Product.objects.filter(
    #         product_parent__slug = obj.slug
    #     )
        
    #     if product_variant_qs:
    #         image_list = obj.images
            
    #         for product_variant in product_variant_qs:
    #             if product_variant.images:
    #                 try:
    #                     image_list.append(product_variant.images[0])
    #                 except:
                        
    #                     image_list = image_list
        
    #     return image_list
    
    
    def get_images(self, obj):
        images = []
       
        product_variant_qs = Product.objects.filter(
            product_parent__slug = obj.slug
        )
        if product_variant_qs:
            images = obj.images
            
            for product_variant in product_variant_qs:
                if product_variant.images:
                    try:
                        images.append(product_variant.images[0])
                    except:
                        pass
        
        return obj.images
class ProductStockCreateUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    product_price_info = serializers.IntegerField(read_only=True)
    stock_in_age = serializers.CharField(read_only=True)
    stock_location = serializers.CharField(write_only=True)
    stock_in_date = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = ProductStock
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True) 
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["product_price_info"] = ProductPriceInfoSerializer(read_only=True)
        return super(ProductStockCreateUpdateSerializer, self).to_representation(instance)
            

class ProductStockListSerializer(serializers.ModelSerializer):
    product_price_info = serializers.SerializerMethodField(read_only=True)
    stock_in_age = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display')
    stock_location = OfficeLocationLiteSerializer(read_only = True)
    status_color = serializers.SerializerMethodField(read_only=True)
    
    
    class Meta:
        model = ProductStock
        fields = [
            'id',
            'barcode',
            'barcode',
            'stock_in_age',
            'stock_in_date',
            'status_display',
            'status_color',
            'product_price_info',
            'stock_location',
                  ]
        
    def get_stock_in_age(self, obj):
        
        stock_in_age = 0
        if obj.status == 'SOLD':
            stock_in_age = obj.stock_in_age
            
        else:
            today = timezone.now()
            stock_in_date = obj.stock_in_date
            if stock_in_date:
                delta = today - stock_in_date
            
                # Extract days, hours, and minutes
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                stock_in_age = f'{days} Days {hours} Hours {minutes} Minutes'

        return stock_in_age
        
    def get_product_price_info(self,obj):
        buying_price = 0.0
        msp = 0.0
        mrp = 0.0
        name = '-'
        image = settings.NOT_FOUND_IMAGE
        
        if obj.product_price_info:
            if obj.product_price_info.product:
                name = obj.product_price_info.product.name
                if obj.product_price_info.product.images:
                    image = obj.product_price_info.product.images[0]
        
        if obj.product_price_info:
            buying_price = obj.product_price_info.buying_price
            msp = obj.product_price_info.msp
            mrp = obj.product_price_info.mrp
        
        context = {
            'name':name,
            'image':image,
            'buying_price':buying_price,
            'msp':msp,
            'mrp':mrp,
        }
        return context
    
    def get_status_color(self, obj):
        return BARCODE_STATUS_DARK_COLORS.get(obj.status, "#FF0000")
    
class ProductStockDownloadListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    stock_in_age = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = ProductStock
        fields = "__all__"
        
    def get_stock_in_age(self, obj):
        
        stock_in_age = 0
        if obj.status == 'SOLD':
            stock_in_age = obj.stock_in_age
            
        else:
            today = timezone.now()
            stock_in_date = obj.stock_in_date
            if stock_in_date:
                delta = today - stock_in_date
            
                # Extract days, hours, and minutes
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                stock_in_age = f'{days} Days {hours} Hours {minutes} Minutes'

        return stock_in_age
        
class ProductStockLiteSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    product_name = serializers.CharField(source='product_price_info.product.name')
    class Meta:
        model = ProductStock
        fields = [
            'id',
            'barcode',
            'status',
            'status_display',
            'product_name',
                  ]
        
class ProductStockLogSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    stock_in_age = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductStockLog
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        return super(ProductStockLogSerializer, self).to_representation(instance)
    
    def get_stock_in_age(self, obj):
        stock_in_age = None
        if obj.stock_in_date:
            now = timezone.now()
            if isinstance(obj.stock_in_date, str):
                stock_in_date = datetime.strptime(obj.stock_in_date, '%m/%d/%Y %I:%M %p')
            else:
                stock_in_date = obj.stock_in_date
            delta = now - stock_in_date
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            stock_in_age = f'{days} Days {hours} Hours {minutes} Minutes'
            
            obj.stock_in_age = stock_in_age
            obj.save()

        return stock_in_age

class ProductStockSerializer(serializers.ModelSerializer):
    product_price_info = serializers.IntegerField(read_only=True)
    stock_location = serializers.IntegerField(read_only=True)
    product_stock_logs = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display')
    stock_in_age = serializers.SerializerMethodField(read_only=True)
    warranty_details = serializers.SerializerMethodField(read_only=True)
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    
    class Meta:
        model = ProductStock
        fields = [
            'id',
            'barcode',
            'status',
            'status_display',
            'stock_in_date',
            'stock_in_age',
            'is_active',
            'product_price_info',
            'stock_location',
            'product_stock_logs',
            'warranty_details',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
        ]
        
    def to_representation(self, instance):
        self.fields["product_price_info"] = ProductPriceInfoSerializer(read_only=True)
        self.fields["stock_location"] = OfficeLocationListSerializer(read_only=True)
        return super(ProductStockSerializer, self).to_representation(instance)
    
    def get_warranty_details(self, obj):
        warranty_details = None
        
        if obj.product_price_info:
            if obj.product_price_info.product.product_warrantys:
                warranty_qs = obj.product_price_info.product.product_warrantys.order_by('warranty_type')
                
                serializer = ProductWarrantyListSerializer(warranty_qs, many = True)
                
                return serializer.data
            
        return warranty_details
    
    def get_stock_in_age(self, obj):
        stock_in_age = None
        if obj.stock_in_date:
            now = timezone.now()
            stock_in_date = obj.stock_in_date
            delta = now - stock_in_date
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            stock_in_age = f'{days} Days {hours} Hours {minutes} Minutes'
        return stock_in_age
    
    def get_product_stock_logs(self, obj):
        if obj.product_stock_logs:
            logs = obj.product_stock_logs.order_by('-stock_in_date__date')
            previous_stock_in_date = None
            
            for log in logs:
                if previous_stock_in_date:
                    delta = log.stock_in_date - previous_stock_in_date
                    days = delta.days
                    hours, remainder = divmod(delta.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    log.stock_in_age = f'{days} Days {hours} Hours {minutes} Minutes {seconds} Seconds'
                previous_stock_in_date = log.stock_in_date
            
            serializer = ProductStockLogSerializer(instance=logs.order_by('-stock_in_date__date'), many=True)
            return serializer.data
        return None



class ProductStockSerializer2(serializers.ModelSerializer):
    product_slug = serializers.CharField(source='product_price_info.product.slug', read_only=True)
    msp = serializers.FloatField(source='product_price_info.msp', read_only=True)

    class Meta:
        model = ProductStock
        fields = ['barcode', 'product_slug','msp']

class ProductStockLogDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStockLog
        fields = [
            'product_stock',
            'stock_location_info',
            'current_status',
            'current_status_display',
            'previous_status',
            'previous_status_display',
            'remarks',
            'is_active',
            'stock_status_change_by_info',
            'stock_in_date',
            'stock_in_age',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
class BarcodePrintSerializer(serializers.Serializer):
    product_code = serializers.CharField()
    quantity = serializers.IntegerField(default = 1)

class SameBarcodePrintSerializer(serializers.Serializer):
    barcode = serializers.CharField()



class ProductStockTransferCreateSerializer(serializers.ModelSerializer):
    from_shop = serializers.CharField(required = True)
    to_shop = serializers.CharField(required = True)
    product_stock = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        model = ProductStockTransfer
        fields = [
            'id',
            'status',
            'stock_transfer_type',
            'product_stock',
            'from_shop',
            'to_shop',
            'remarks',
            'is_active',
        ]
        
class ProductStockTransferReceivedSerializer(serializers.Serializer):
    barcode = serializers.CharField()
class ProductStockTransferUpdateSerializer(serializers.ModelSerializer):
    status_change_reason = serializers.CharField()
    class Meta:
        model = ProductStockTransfer
        fields = [
            'id',
            'status',
            'status_change_reason'
        ]
        
class ProductStockTransferListSerializer(serializers.ModelSerializer):
    from_shop = OfficeLocationLiteSerializer(read_only=True)
    to_shop = OfficeLocationLiteSerializer(read_only=True)
    approved_by = EmployeeInformationBaseSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    stock_transfer_type_display = serializers.CharField(source='get_stock_transfer_type_display', read_only=True)
    
    total_barcode = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductStockTransfer
        fields = [
            'id',
            'created_at',
            'total_barcode',
            'requisition_no',
            'status',
            'status_display',
            'stock_transfer_type',
            'stock_transfer_type_display',
            'from_shop',
            'to_shop',
            'approved_by',
            'created_at',
        ]
    
    def get_total_barcode(self, obj):
        
        total_barcode = '0'
        if obj.product_stock:
            # barcode_list = obj.product_stock.values_list('barcode', flat = True)
            total_barcode = obj.product_stock.all().count()
            
        return total_barcode
    
class ProductStockTransferSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    approved_by = serializers.IntegerField(read_only=True)
    product_stock = serializers.SerializerMethodField(read_only=True)
    
    
    mismatch_barcode_list = serializers.SerializerMethodField(read_only=True)
    not_received_barcode_list = serializers.SerializerMethodField(read_only=True)
    received_barcode_list = serializers.SerializerMethodField(read_only=True)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    stock_transfer_type_display = serializers.CharField(source='get_stock_transfer_type_display', read_only=True)
    
    class Meta:
        model = ProductStockTransfer
        fields = [
            'id',
            'requisition_no',
            'status',
            'status_display',
            'stock_transfer_type',
            'stock_transfer_type_display',
            'received_barcode_list',
            'not_received_barcode_list',
            'mismatch_barcode_list',
            'product_stock',
            'from_shop',
            'to_shop',
            'approved_by',
            'remarks',
            'is_active',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
        ]
        
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["approved_by"] = EmployeeInformationBaseSerializer(read_only=True)
        self.fields["from_shop"] = OfficeLocationListSerializer(read_only=True)
        self.fields["to_shop"] = OfficeLocationListSerializer(read_only=True)
        
        return super(ProductStockTransferSerializer, self).to_representation(instance)
    
    def get_product_stock(self, obj):
        if obj.product_stock:
            serializer = ProductStockListSerializer(obj.product_stock, many = True)
            return serializer.data
        return None
    
    def get_mismatch_barcode_list(self, obj):
        mismatch_barcode_list = None
        try:
            if obj.mismatch_barcode_list:
                mismatch_barcode_list = eval(obj.mismatch_barcode_list)
        except:
            pass
        return mismatch_barcode_list
    
    def get_not_received_barcode_list(self, obj):
        not_received_barcode_list = None
        try:
            if obj.not_received_barcode_list:
                not_received_barcode_list = eval(obj.not_received_barcode_list)
        except:
            pass
        return not_received_barcode_list
    
    def get_received_barcode_list(self, obj):
        received_barcode_list = None
        try:
            if obj.received_barcode_list:
                received_barcode_list = eval(obj.received_barcode_list)
        except:
            pass
        return received_barcode_list
            

class ProductStockTransferLogSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    
    class Meta:
        model = ProductStockTransferLog
        fields = '__all__'
       
class ProductStockTransferDetailsSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    approved_by = EmployeeInformationBaseSerializer(read_only=True)
    from_shop = OfficeLocationListSerializer(read_only=True)
    to_shop = OfficeLocationListSerializer(read_only=True)
    product_stock = ProductStockLiteSerializer(many=True, read_only=True)
    product_stock_transfer_logs = serializers.SerializerMethodField(read_only=True)
    
    mismatch_barcode_list = serializers.SerializerMethodField(read_only=True)
    not_received_barcode_list = serializers.SerializerMethodField(read_only=True)
    received_barcode_list = serializers.SerializerMethodField(read_only=True)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    stock_transfer_type_display = serializers.CharField(source='get_stock_transfer_type_display', read_only=True)
    
    class Meta:
        model = ProductStockTransfer
        fields = '__all__'
    
    def get_product_stock_transfer_logs(self, obj):
        if obj.product_stock_transfer_logs:
            serializer = ProductStockTransferLogSerializer(
                instance=obj.product_stock_transfer_logs, many = True
                )
            
        return serializer.data
    
    def get_mismatch_barcode_list(self, obj):
        mismatch_barcode_list = None
        try:
            if obj.mismatch_barcode_list:
                mismatch_barcode_list = eval(obj.mismatch_barcode_list)
        except:
            mismatch_barcode_list = None
            
        return mismatch_barcode_list
    
    def get_not_received_barcode_list(self, obj):
        not_received_barcode_list = None
        print("ddd", not_received_barcode_list)
        
        try:
            if obj.not_received_barcode_list:
                not_received_barcode_list = eval(obj.not_received_barcode_list)
        except:
            not_received_barcode_list = None
            
        return not_received_barcode_list
    
    def get_received_barcode_list(self, obj):
        received_barcode_list = None
        try:
            if obj.received_barcode_list:
                received_barcode_list = eval(obj.received_barcode_list)
        except:
            pass
        return received_barcode_list
    
class ProductRequisitionProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    requisition_item = serializers.SerializerMethodField(read_only = True)
    product_stock_details = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'image',
            'slug',
            'minimum_stock_quantity', 
            'requisition_item', 
            'product_stock_details', 
        ]
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        
        if obj.images:
            image_url = random.choice(obj.images)
            
        return image_url
        
    def get_product_stock_details(self, obj):
        product_stock_details = []
        
        qs = ProductStock.objects.filter(
            product_price_info__product__slug = obj.slug
        )
        if qs:
            serializer = ProductStockLiteSerializer(instance=qs, many = True)
            return serializer.data
        
            
        return product_stock_details
    
    def get_requisition_item(self, obj):
        total_sold_item = 0.0
        total_required_item = 0.0
        total_current_stock_item = 0.0
        
        if obj.id%2 == 0:
            total_sold_item = 0.0
            total_current_stock_item = 0.0
            total_required_item = 0.0
            
        sold_product_stock_qs = Product.objects.filter(slug = obj.slug, product_price_infos__product_stocks__status = 'SOLD')
        
        product_stock_qs = Product.objects.filter(slug = obj.slug, product_price_infos__product_stocks__status__in  = ['ACTIVE', 'FAULTY' ])
      
        if sold_product_stock_qs:
            total_sold_item = sold_product_stock_qs.count()
            
        if product_stock_qs:
            total_current_stock_item = product_stock_qs.count()
        
        context = {
            'total_current_stock_item':total_current_stock_item,
            'total_sold_item':total_sold_item,
            'total_required_item':total_required_item
        }
        
        return context
    
class ProductRequisitionShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = [
            'id',
            'name',
            'slug',
            'store_no',
            'primary_phone'
        ]    
        
class ProductRequisitionListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = ProductStockTransfer
        fields = [
            'id',
            'requisition_no',
            'status',
            'status_display',
        ]
        
class ProductRequisitionListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    shop = OfficeLocationListSerializer()
    # product = ProductListSerializer()
    class Meta:
        model = ProductStockRequisition
        fields = [
                  'id',
                  'requisition_no',
                  'status',
                  'status_display',
                  'shop',
                #   'product',
                  'total_need_quantity',
                  ]
        
class ProductRequisitionItemCreateSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(required = True)

    class Meta:
        model = ProductStockRequisitionItem
        fields = [
            'id',
            'product_slug',
            'needed_quantity'
        ]       
        
         
class ProductRequisitionCreateSerializer(serializers.ModelSerializer):
    employee_slug = serializers.CharField(required = True)
    item_list = ProductRequisitionItemCreateSerializer(many = True)

    class Meta:
        model = ProductStockRequisition
        fields = [
            'id',
            'employee_slug',
            'item_list',
        ]
         
         
class ProductRequisitionItemUpdateSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    product_slug = serializers.CharField(required = True)
    order_status_reason = serializers.CharField(required = False)

    class Meta:
        model = ProductStockRequisitionItem
        fields = [
            'id',
            'item_id',
            'status',
            'order_status_reason',
            'product_slug',
            'approved_quantity',
            'needed_quantity'
        ]       
        
        
class ProductRequisitionUpdateSerializer(serializers.ModelSerializer):
    item_list = ProductRequisitionItemUpdateSerializer(many = True)
    order_status_reason = serializers.CharField(required = False)

    class Meta:
        model = ProductStockRequisition
        fields = [
            'id',
            'status',
            'order_status_reason',
            'item_list',
        ]   
        
class ProductRequisitionTransferSerializer(serializers.ModelSerializer):
    from_shop = serializers.CharField(required = True)
    to_shop = serializers.CharField(required = True)
    product_stock = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        model = ProductStockTransfer
        fields = [
            'id',
            'product_stock',
            'from_shop',
            'to_shop',
            'remarks'
        ]

class EmployeeInformationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeInformation
        fields = [
            'id',
            'employee_id',
            'name',
            'image',
                  ]
        
        
class ProductRequisitionItemDetailsSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display'
                                           , read_only=True)
    
    status_change_by = EmployeeInformationListSerializer()
    product = ProductListSerializer()
    class Meta:
        model = ProductStockRequisitionItem
        fields = '__all__' 
        
class ProductRequisitionDetailsSerializer(serializers.ModelSerializer):
    shop = OfficeLocationListSerializer()
    status_change_by = EmployeeInformationListSerializer()
    approved_by = EmployeeInformationListSerializer()
    product_stock_requisition_items = ProductRequisitionItemDetailsSerializer(many=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    

    class Meta:
        model = ProductStockRequisition
        fields = '__all__'
        
        
class PublicProductDetailsSerializer(serializers.ModelSerializer):
    category = CategoryLiteSerializer(read_only=True, many=True)
    sub_category = CategoryLiteSerializer(read_only=True, many=True)
    price_details = serializers.SerializerMethodField(read_only = True)
    product_attribute_value = serializers.SerializerMethodField(read_only = True)
    review_ratting_details = serializers.SerializerMethodField(read_only = True)
    product_warranty_details = serializers.SerializerMethodField(read_only = True)
    total_order = serializers.SerializerMethodField(read_only = True)
    product_variant = serializers.SerializerMethodField(read_only = True)
    breadcrumb = serializers.SerializerMethodField(read_only = True)
    # short_description = serializers.SerializerMethodField(read_only = True)
    # description = serializers.SerializerMethodField(read_only = True)
    images = serializers.SerializerMethodField(read_only = True)
    # integrity_guaranteed = serializers.SerializerMethodField(read_only = True) 
    
    class Meta:
        model = Product
        fields = "__all__"
       
    def to_representation(self, instance):
        self.fields["product_parent"] = ProductListSerializer(read_only=True)
        self.fields["gift_product"] = ProductListSerializer(read_only=True)
        self.fields["brand"] = BrandListSerializer(read_only=True)
        self.fields["supplier"] = SupplierSerializer(read_only=True)
        self.fields["selling_tax_category"] = TaxCategorySerializer(read_only=True)
        self.fields["buying_tax_category"] = TaxCategorySerializer(read_only=True)
        self.fields["category"] = CategoryLiteSerializer(read_only=True, many=True)
        self.fields["sub_category"] = CategoryLiteSerializer(read_only=True, many=True)
        return super(PublicProductDetailsSerializer, self).to_representation(instance)
    
    
    # def get_integrity_guaranteed(self, obj):
    #     if obj:
    #         # context = {
    #         #     "quality": "yellow",
    #         #     "authenticity": "yellow", 
    #         #     "seller_reliability": "green"
    #         #     }
    #         context = obj.integrity_guaranteed
            
    #     return context
    
    def get_images(self, obj):

        image_list = [
            settings.NOT_FOUND_IMAGE,
            settings.NOT_FOUND_IMAGE
                ] 
        
        if obj.images:
            images = obj.images
            
        else:
            images = image_list
            
        product_variant_qs = Product.objects.filter(
            product_parent__slug = obj.slug
        )
        
        if product_variant_qs:
            if obj.images:
                images = obj.images
            
            for product_variant in product_variant_qs:
                if product_variant.images:
                    images.append(product_variant.images[0])
        
        return images
    
    
    def get_product_warranty_details(self, obj):
        if obj.product_warrantys:
            serializer = ProductWarrantySerializer(instance = obj.product_warrantys, many = True)
            return serializer.data
        return None
    
    # def get_short_description(self, obj):
    #     short_description = f"<p>HP EliteBook 840 G3 Ci5 Touch<br />Intel Core i5-6200U (2.3 GHz )<br />ডিসপ্লে 14.1&Prime;&nbsp;<br />8 GB DDR4-2400 SDRAM<br />256 GB M.2 SATA SSD<br />Intel &reg; UHD গ্রাফিক্স 520</p> <br> <br> <p>HP EliteBook 840 G3 Ci5 Touch<br />Intel Core i5-6200U (2.3 GHz )<br />ডিসপ্লে 14.1&Prime;&nbsp; HP EliteBook 840 G3 Ci5 Touch HP EliteBook 840 G3 Ci5 Touch"
        
    #     return short_description
    
    # def get_description(self, obj):
    #     description = "<p><strong>Model:</strong> Vostro 14 3400<br /><strong>Processor:</strong> Intel Core i7-1165G7 Processor (12MB Cache, 2.80 GHz up to 4.70 GHz)<br /><strong>Display:</strong> 14.0-inch FHD (1920 x 1080) Anti-glare LED Backlight Non-touch Narrow Border WVA Display<br /><strong>Memory:</strong> 8GB, 1x8GB, DDR4 RAM<br /><strong>Storage:</strong> 512GB M.2 PCIe NVMe Solid State Drive<br /><strong>Graphics:</strong> NVIDIA GeForce MX350 with 2GB GDDR5 graphics memory<br /><strong>Operating System:</strong> Free DOS<br /><strong>Battery:</strong> 3-Cell Battery, 40WHr (Integrated)<br /><strong>Adapter:</strong> 45 Watt AC Adaptor<br /><strong>Keyboard:</strong> Dark Grey Keyboard Non-Backlit<br /><strong>WebCam:</strong> 1280x720 Intergrated HD Webcam<br /><strong>Card Reader:</strong> 1x 3-in-1 SD Media Card Reader<br /><strong>Wi-Fi:</strong> 802.11ac 2x2 WiFi<br /><strong>Bluetooth:</strong> Yes<br /><strong>USB (s):</strong> 1x USB 3.2 Gen 1 Type-C (Data only)<br />2x USB 3.2 Gen 1 Type-A<br /><strong>HDMI:</strong> 1x HDMI 1.4b<br /><strong>Audio Jack Combo:</strong> 3.5 mm Headset Jack<br /><strong>Dimensions (W x D x H):</strong> Height: Front: 0.66 '(16.74 mm) Rear: 0.7 (17.9 mm)<br />Width: 12.65 (321.3 mm)<br />Depth: 8.51 (216.2 mm)<br /><strong>Weight:</strong> 3.03 lb (1.36 kg)<br /><strong>Color(s):</strong> Black</p>"
        
    #     return description

    
    def get_breadcrumb(self, obj):
        # Default breadcrumb values
        product_group_name = 'Product-Group/Name/'
        product_group_slug = 'Product-Group/Sug/'
        product_group_path = 'Product-Group/Path/'
        
        category_name = 'Category/Name/'
        category_slug = 'Category/Sug/'
        category_path = 'Category/Path/'
        
        sub_category_name = 'Sub-Category/Name/'
        sub_category_slug = 'Sub-Category/Sug/'
        sub_category_path = 'Sub-Category/Path/'
        
        product_name = 'Product/Name/'
        product_slug = 'Product/Sug/'
        product_path = 'Product/Path/'

        # Initialize breadcrumbs list
        data_list = [
            {
                'name': "Home",
                'slug': "/",
                'path': "/",
            }
        ]

        # Fetch related objects safely
        sub_category = obj.sub_category.last() if obj.sub_category.exists() else None
        category = obj.category.last() if obj.category.exists() else None
        product_group = category.category_group if category and category.category_group else None

        # Set breadcrumb values based on existing objects
        if product_group:
            product_group_name = product_group.name
            product_group_slug = product_group.slug
            product_group_path = f"/product-category/{product_group.slug}"
            data_list.append({
                'name': product_group_name,
                'slug': product_group_slug,
                'path': product_group_path,
            })
        
        if category:
            category_name = category.name
            category_slug = category.slug
            if product_group:
                category_path = f"/product-category/{product_group.slug}/{category.slug}"
            else:
                category_path = f"/product-category/{category.slug}"
            data_list.append({
                'name': category_name,
                'slug': category_slug,
                'path': category_path,
            })

        if sub_category:
            sub_category_name = sub_category.name
            sub_category_slug = sub_category.slug
            if category and product_group:
                sub_category_path = f"/product-category/{product_group.slug}/{category.slug}/{sub_category.slug}"
            elif category:
                sub_category_path = f"/product-category/{category.slug}/{sub_category.slug}"
            else:
                sub_category_path = f"/product-category/{sub_category.slug}"
            data_list.append({
                'name': sub_category_name,
                'slug': sub_category_slug,
                'path': sub_category_path,
            })

        # Always include the product breadcrumb if obj exists
        if obj:
            product_name = obj.name
            product_slug = obj.slug
            if sub_category and category and product_group:
                product_path = f"/product-category/{product_group.slug}/{category.slug}/{sub_category.slug}/{obj.slug}"
            elif sub_category and category:
                product_path = f"/product-category/{category.slug}/{sub_category.slug}/{obj.slug}"
            elif category:
                product_path = f"/product-category/{category.slug}/{obj.slug}"
            else:
                product_path = f"/product-category/{obj.slug}"
            data_list.append({
                'name': product_name,
                'slug': product_slug,
                'path': '',
            })

        return data_list



    def get_product_attribute_value(self, obj):
        product_attribute_value = []
        
        if obj.product_attribute_value:
            product_variant_qs = Product.objects.filter(product_parent__slug = obj.slug)
            
            product_attribute_qs = ProductAttribute.objects.filter(
                Q(name__in = obj.product_attribute_value.all().values_list('product_attribute__name', flat=True))
                | Q(name__in = product_variant_qs.values_list('product_attribute_value__product_attribute__name', flat=True))
            )
            
            product = obj
            product_attribute_list = product_attribute_qs
            
            product_attribute_value = parent_product_attribute_value_list(product, product_attribute_list)
            
        return product_attribute_value
    
    def get_product_variant(self, obj):
        product_variant_qs = Product.objects.filter(product_parent__slug = obj.slug)
        
        if product_variant_qs:
            serializer = ProductVariantListSerializer(instance=product_variant_qs, many = True)
            return serializer.data
        
        return None
    
    def get_price_details(self, obj):
        product_price = product_price_details(product = obj, product_price_type='ECOMMERCE')
            
        return product_price
    
    def get_review_ratting_details(self, obj):
        context = {}
        total_customer_review = 0
        all_rating = {}
        total_rating = 0.0
        review_list = []
        
        
        # all_rating = {
        #     'five_star': 1044,
        #     'four_star': 34,
        #     'three_star': 534,
        #     'two_star': 1254,
        #     'one_star': 1534,
        # }
        # review_list.append({
        #     'review_by': 'admin@gmail.com',
        #     'message': 'Superb sweatshirt. I loved it. It is for winter.',
        #     'review_at': 'Jan 08 at 02:46 pm'
        # })

        # review_list.append({
        #     'review_by': 'remon@gmail.com',
        #     'message': 'Great at this price, Product quality and look are awesome.',
        #     'review_at': 'Jan 08 at 02:46 pm'
        # })
        
        context = {
            'total_customer_review':total_customer_review,
            'total_rating':total_rating,
            'all_rating':all_rating,
            'review_list':review_list,
        }
        
        return context
    
    def get_total_order(self, obj):
        total_order = 0
        
        return total_order
    

class ProductVariantProductAttributeValueCreateSerializer(serializers.Serializer):
    product_attribute = serializers.CharField()
    product_attribute_value = serializers.CharField()

class ProductVariantCreateSerializer(serializers.ModelSerializer):
    product_attribute = ProductVariantProductAttributeValueCreateSerializer(many = True)
    product_price = ProductPriceInfoCreateSerializer(many = True)
    
    class Meta:
        model = Product
        fields = [
            'sku',
            'product_code',
            'product_attribute',
            'product_price',
            "images",
                ]
        
class PublicProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    bn_name = serializers.SerializerMethodField(read_only = True)
    price_details = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'bn_name',
            'slug',
            'image',
            'sku',
            'is_cart_disabled',
            'price_details',
        ]
        
    def get_image(self, obj):
        image_url = product_image(product = obj)
        return image_url
    
    def get_bn_name(self, obj):
        bn_name = obj.name
        if obj.translation:
            try:
                bn_name = obj.translation.get("translation")
            except:
                pass
        return bn_name
    
    def get_price_details(self, obj):
        # Asynchronous operation
        product_price = product_price_details(product=obj, product_price_type='ECOMMERCE')
        
        return product_price
        
class PublicOnTheGoProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    price_details = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'price_details',
        ]
        
    def get_image(self, obj):
        image_url = product_image(product = obj)
        return image_url
    
    def get_price_details(self, obj):
        price_details = product_price_details(product=obj, product_price_type='POINT_OF_SELL')
        return price_details
    
    
class CustomerProductReview(serializers.ModelSerializer):
    product = PublicProductListSerializer(read_only = True)
    class Meta:
        model = ProductReview
        fields = [
            'id',
            'product',
            'rating',
            'review_text',
        ]
        
class ProductAttributeListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = ProductAttributeValue
        fields = [
            'id',
            'value',
            'slug',
            'image',
        ]
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        if obj.products:
            image_url = product_image(product = obj.products.all().last())
        return image_url
        
        
class ProductStockTransferDownloadListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    stock_transfer_type_display = serializers.CharField(source='get_stock_transfer_type_display')
    from_shop_name = serializers.SerializerMethodField()
    to_shop_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductStockTransfer
        fields = "__all__"
        
    def get_from_shop_name(self,obj):
        from_shop_name = '-'
        if obj.from_shop:
            from_shop_name = obj.from_shop.name
        return from_shop_name
    
    def get_to_shop_name(self,obj):
        to_shop_name = '-'
        if obj.to_shop:
            to_shop_name = obj.to_shop.name
        return to_shop_name
    
    def get_approved_by_name(self,obj):
        approved_by_name = '-'
        if obj.approved_by:
            approved_by_name = obj.approved_by.name
        return approved_by_name
    
    def get_product_stock(self,obj):
        product_stock_list = '-'
        if obj.product_stock:
            if obj.product_stock.all().values_list('barcode', flat=True):
                barcode_list = obj.product_stock.all().values_list('barcode', flat=True)
                if barcode_list:  # Check if the barcode list is not empty
                    product_stock_list = list(barcode_list)
        return product_stock_list
    
    
class ShopWiseZeroStockLogSerializer(serializers.ModelSerializer):
    product = ProductLiteSerializer(read_only = True)
    office_location = OfficeLocationLiteSerializer(read_only = True)
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    
    class Meta:
        model = ShopWiseZeroStockLog
        fields = "__all__"