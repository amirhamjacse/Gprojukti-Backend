from datetime import timedelta
import random
from django.conf import settings
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer
from discount.models import *
from django.db.models import Q
from drf_extra_fields.fields import Base64FileField, Base64ImageField
from gporjukti_backend_v2.settings import BASE_URL
from product_management.models.product import Product

from user.serializers import BaseSerializer
from django.utils import timezone

from utils.base import product_image
from utils.calculate import offer_check


class DiscountListSerializer(serializers.ModelSerializer):
    discount_details = serializers.SerializerMethodField(read_only =True)
    image = serializers.SerializerMethodField(read_only =True)
    amount_type_display = serializers.CharField(source='get_amount_type_display', read_only =  True)
    discount_type_display = serializers.CharField(source='get_discount_type_display', read_only =  True)
    discount_status_display = serializers.CharField(source='get_discount_status_display', read_only =  True)
    
    class Meta:
        model = Discount
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'discount_status',
            'discount_status_display',
            'discount_type',
            'discount_type_display',
            'amount_type',
            'amount_type_display',
            'discount_details',
            'terms_and_conditions',
            'meta',
                  ]
        
    def get_discount_details(self, obj):
        context = offer_check(obj)
        return context
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        
        if obj.image:
            image_url = obj.image 
        return image_url
        
class DiscountSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only =  True)
    amount_type_display = serializers.CharField(source='get_amount_type_display', read_only =  True)
    discount_type_display = serializers.CharField(source='get_discount_type_display', read_only =  True)
    discount_status_display = serializers.CharField(source='get_discount_status_display', read_only =  True)
    
    image = Base64ImageField(required=False)
    start_date = serializers.DateTimeField(format="%m/%d/%Y %I:%M %p")
    end_date = serializers.DateTimeField(format="%m/%d/%Y %I:%M %p")
    
    start_time = serializers.DateTimeField(format="%I:%M %p")
    end_time = serializers.DateTimeField(format="%I:%M %p")
    

    class Meta:
        model = Discount 
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'schedule_type_display',
            'amount_type',
            'discount_amount',
            'amount_type_display',
            'discount_type',
            'discount_type_display',
            'discount_status',
            'discount_status_display',
            'company',
            'remarks',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
                  ]

    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(DiscountSerializer, self).to_representation(instance)
    
   
class DiscountDetailsSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    company = CompanyLiteSerializer(read_only=True)
    
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only =  True)
    amount_type_display = serializers.CharField(source='get_amount_type_display', read_only =  True)
    discount_type_display = serializers.CharField(source='get_discount_type_display', read_only =  True)
    discount_status_display = serializers.CharField(source='get_discount_status_display', read_only =  True)
    
    class Meta:
        model = Discount
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'schedule_type_display',
            'amount_type',
            'amount_type_display',
            'discount_type',
            'discount_type_display',
            'discount_status',
            'discount_status_display',
            'company',
            'remarks',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
                  ]

    
class PromoCodeListSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only=True)
    updated_by = BaseSerializer(read_only=True)
    promo_code_details = serializers.SerializerMethodField(read_only =True)
    
    class Meta:
        model = PromoCode
        fields = [
            'id',
            'promo_code',
            'slug',
            'image',
            'promo_code_details',
            'created_by',
            'updated_by',
        ]
        
    def get_promo_code_details(self, obj):
        context = offer_check(obj)
        return context
    
class PromoCodeSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only =  True)
    amount_type_display = serializers.CharField(source='get_amount_type_display', read_only =  True)
    promo_type_display = serializers.CharField(source='get_promo_type_display', read_only =  True)
    
    image = Base64ImageField(required=False)
    

    class Meta:
        model = PromoCode
        fields = [
            'id',
            'promo_code',
            'slug',
            'image',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'schedule_type_display',
            'amount_type',
            'discount_amount',
            'amount_type_display',
            'promo_type',
            'promo_type_display',
            'minimum_purchase_amount',
            'maximum_purchase_amount',
            'maximum_use_limit',
            'is_for_lifetime',
            'is_for_all',
            'company',
            'remarks',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
                  ]

    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(PromoCodeSerializer, self).to_representation(instance)
        
        

    
class PromoProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'product_code'
        ]
        
    def get_image(self, obj):
        image_url = product_image(product = obj)
        return image_url
        
class PromoCodeDetailsSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only =  True)
    amount_type_display = serializers.CharField(source='get_amount_type_display', read_only =  True)
    promo_type_display = serializers.CharField(source='get_promo_type_display', read_only =  True)
    
    # image = Base64ImageField(required=False)
    
    product_list = serializers.SerializerMethodField(read_only =True)
    

    class Meta:
        model = PromoCode
        fields = [
            'id',
            'promo_code',
            'slug',
            'image',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'schedule_type_display',
            'amount_type',
            'discount_amount',
            'amount_type_display',
            'promo_type',
            'promo_type_display',
            'minimum_purchase_amount',
            'maximum_purchase_amount',
            'maximum_use_limit',
            'company',
            'product_list',
            'remarks',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
                  ]

    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(PromoCodeDetailsSerializer, self).to_representation(instance)
        
    def get_product_list(self, obj):
        product_list = []
        if obj.promo_code:
            product_qs = Product.objects.filter(product_price_infos__promo_code__promo_code = obj.promo_code)
            serializer = PromoProductListSerializer(product_qs, many = True)
            return serializer.data
        return product_list
        


class PromoCodeUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only =  True)
    amount_type_display = serializers.CharField(source='get_amount_type_display', read_only =  True)
    promo_type_display = serializers.CharField(source='get_promo_type_display', read_only =  True)
    
    image = Base64ImageField(required=False)
    

    class Meta:
        model = PromoCode
        fields = [
            'id',
            'image',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'schedule_type_display',
            'amount_type',
            'discount_amount',
            'amount_type_display',
            'promo_type',
            'promo_type_display',
            'minimum_purchase_amount',
            'maximum_purchase_amount',
            'maximum_use_limit',
            'is_for_lifetime',
            'is_for_all',
            'company',
            'remarks',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
                  ]

    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(PromoCodeUpdateSerializer, self).to_representation(instance)
    
    
class ProductSlugListSerializer(serializers.Serializer):
    product_slug = serializers.CharField()  
    quantity = serializers.IntegerField(default = 1)  
    
class CheckPromoCodeSerializer(serializers.ModelSerializer):
    product_list = ProductSlugListSerializer(many = True)
    order_type = serializers.CharField(default='ECOMMERCE_SELL') 
    
    class Meta:
        model = PromoCode
        fields = [
            'promo_code',
            'order_type',
            'product_list'
            ]
        
class DiscountAddCategorySerializer(serializers.Serializer):
    slug = serializers.CharField()
    
class DiscountAddProductSerializer(serializers.Serializer):
    slug = serializers.CharField()
    
class productWiseDiscountPromoCodeAddSerializer(serializers.Serializer):
    category = DiscountAddCategorySerializer(many = True)
    product = DiscountAddProductSerializer(many = True)
    
    
    
class DiscountProductListSerializer(serializers.ModelSerializer):
    price_details =  serializers.SerializerMethodField(read_only = True)
    image =  serializers.SerializerMethodField(read_only = True)
    
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
        image_url = settings.NOT_FOUND_IMAGE
        
        if obj.images:
            image_url = product_image(product = obj) 
        return image_url
        
    def get_price_details(self, obj):
        context = {}
        
        msp = 3633
        mrp = 4357
        discount_amount = 0.0
        after_discount_price = 0.0
        tax_amount = 0.0
        tax_value = 0.0
        gsheba_amount = 0.0
        tax_value_title = None
        discount_title = None
        
        if obj.is_out_of_stock:
            is_out_of_stock = True
            context = {
                'is_out_of_stock': is_out_of_stock
            }
            return context
        
        ecommerce_price_qs = obj.product_price_infos.filter(product_price_type = 'ECOMMERCE').last()
        if ecommerce_price_qs:
            msp = ecommerce_price_qs.msp
            mrp = ecommerce_price_qs.mrp
            gsheba_amount = ecommerce_price_qs.gsheba_amount
            
            if ecommerce_price_qs.discount:
                discount_qs = ecommerce_price_qs.discount
                discount = offer_check(discount_qs)
                
                discount_status = discount.get('valid_status')
                discount_amount = discount.get('discount_value')
                
                if discount_status=='Active':
                    if discount_qs.amount_type == 'FLAT':
                        discount_amount =  discount_qs.discount_amount
                    else:
                        discount_amount = (mrp*discount_qs.discount_amount)/100
                        
                    discount_title = discount_qs.name
            
                if obj.selling_tax_category:
                    tax_amount = (after_discount_price * obj.selling_tax_category.value_in_percentage) / 100
                    tax_value = obj.selling_tax_category.value_in_percentage
                    tax_value_title = obj.selling_tax_category.name
       
        after_discount_price = mrp - discount_amount
            
        context = {
            'msp': msp,
            'mrp': mrp,
            'gsheba_amount': gsheba_amount,
            'after_discount_price': after_discount_price,
            'discount_amount': discount_amount,
            'discount_title': discount_title,
            'tax_amount': tax_amount,
            'tax_value': tax_value,
            'tax_value_title': tax_value_title,
        }
            
        return context
    
        
class DiscountWiseProductListSerializer(serializers.ModelSerializer):
    product_list = serializers.SerializerMethodField(read_only = True)
    remaining_days = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Discount
        fields = [
            'id',
            'name',
            'image',
            'product_list',
            'remaining_days'
            ]
        
    def get_remaining_days(self, obj):
        start_date = '2024-01-01'
        end_date = '2024-01-01'
        remaining_days = None
        
        if obj.schedule_type == 'DATE_WISE':
            start_date = obj.start_date
            end_date = obj.end_date
        else:
            start_date = obj.start_time
            end_date = obj.end_time
            
        context = {
            "start_date": start_date,
            "end_date": end_date,
        }
        return context
        
    def get_product_list(self, obj):
        product_qs = Product.objects.filter(product_price_infos__discount = obj)[:3]
        if product_qs:
            serializer = DiscountProductListSerializer(product_qs, many = True)
            return serializer.data
        
        return None
        