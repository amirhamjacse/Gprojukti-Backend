from django.conf import settings
from rest_framework import serializers
from human_resource_management.serializers.employee import EmployeeInformationListSerializer
from location.serializers import OfficeLocationListSerializer
from product_management.serializers.product import ProductListSerializer
from settings_management.models import *
from user.serializers import BaseSerializer
from drf_extra_fields.fields import Base64FileField, Base64ImageField

from utils.base import product_image
from utils.upload_image import image_upload
from django.db.models import IntegerField
from django.db.models.functions import Cast



class SliderListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slider
        fields = [
                  'id',
                  'name',
                  'slug',
                  'image',
                  'serial_no',
                  'url'
                ]
        
        
class SliderCreateUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    
    class Meta:
        model = Slider
        fields = '__all__'
        
    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        if image_file:
            path ='slider'
            image = image_upload(file=image_file, path=path)
            if image:
                return Slider.objects.create(image=image, **validated_data)
        return Slider.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        image = validated_data.get('image')
        if image:
            image_file = validated_data.pop('image', None)
            path = 'slider'
            image = image_upload(file=image_file, path=path)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            if image:
                instance.image = image
            
            instance.save()
        return instance
    
class SliderSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    
    class Meta:
        model = Slider
        fields = '__all__'
        
class ShopDayEndSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    shop = OfficeLocationListSerializer(read_only = True)
    
    class Meta:
        model = ShopDayEnd
        fields = '__all__'
        
class ShopDayEndCreateSerializer(serializers.ModelSerializer):
    shop_slug = serializers.CharField()
    class Meta:
        model = ShopDayEnd
        fields = [
                  'shop_slug',
                  'total_sell_amount',
                  'retail_sell_amount',
                  'retail_gsheba_sell_amount',
                  'panel_partnership',
                  'e_retail_sell_amount',
                  'ecommerce_collection_amount',
                  'corporate_sell_amount',
                  'refund_amount',
                  'warranty_claim_quantity',
                  'gsheba_claim_quantity',
                  'total_b2b_sell_amount',
                  'mfs_collection',
                  'mfs_collection',
                  'currency_collection',
                  'total_bank_deposit_amount',
                  'total_expense_amount',
                ]
        
class NewsLetterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = [
                    'email'  
                ]

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = '__all__'
        
class ShopDayEndMessageSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    employee_information = EmployeeInformationListSerializer(read_only = True)
    office_location = OfficeLocationListSerializer(read_only = True, many=True)
    
    class Meta:
        model = ShopDayEndMessage
        fields = '__all__'
        
class ShopDayEndMessageCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShopDayEndMessage
        fields = [
                    'id',
                    'office_location',
                    'employee_information',
                    'is_message_send',
                    'is_mail_send',
                    'is_active',
                    'remarks',
                ]
        
        
class ShopPanelSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    slug = serializers.CharField(read_only = True)
    
    class Meta:
        model = ShopPanel
        fields = '__all__'
        
        
class AllHookProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'product_code',
        ]
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        if obj.images:
            try:
                image_url = product_image(product = obj)
            except:
                pass
        return image_url
    
    
class ShopPanelHookSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    slug = serializers.CharField(read_only = True)
    product_list = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = ShopPanelHook
        fields = '__all__'
        
    def get_product_list(self, obj):
        
        if  obj.hook_products.all().count() > 0:
            # pass
            hook_products = obj.hook_products.all()
            
            product_qs = Product.objects.filter(id__in = obj.hook_products.all().values_list('product', flat=True))
            
            serializer = AllHookProductListSerializer(product_qs, many=True)
            
            return serializer.data 
        return None
        
        
class HookProductListSerializer(serializers.Serializer): 
    product_slug = serializers.CharField()
    serial_no = serializers.CharField()
    remarks = serializers.CharField()
    is_active = serializers.BooleanField()
    
class ShopPanelHookCreateUpdateSerializer(serializers.ModelSerializer): 
    slug = serializers.CharField(read_only = True)
    shop_panel_slug = serializers.CharField(write_only = True)
    product_list = HookProductListSerializer(write_only = True, many=True)
    
    # created_by = BaseSerializer(read_only = True)
    # updated_by = BaseSerializer(read_only = True)
    class Meta:
        model = ShopPanelHook
        fields = [
                'id',  
                'name',  
                'slug',  
                'serial_no',  
                'is_active',  
                'remarks',  
                'shop_panel_slug',  
                'product_list',  
                ]
        
        
        

class ShopPanelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPanel
        fields = [
                "id",
                "name",
                "slug"
                ]
        
    
class ShopPanelDetailsSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    slug = serializers.CharField(read_only = True)
    shop_panel_hook = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = ShopPanel
        fields = '__all__'
        
        
    def get_shop_panel_hook(self, obj):
        if obj.shop_panel_hooks.exists():
            # shop_panel_hooks = obj.shop_panel_hooks.annotate(
            #     serial_no_int=Cast('serial_no', IntegerField())
            # ).order_by('serial_no_int')
            # shop_panel_hooks = obj.shop_panel_hooks.annotate(
            #     serial_no_int=Cast('serial_no', IntegerField())
            # ).order_by('serial_no_int')
            serializer = ShopPanelHookSerializer(obj.shop_panel_hooks, many=True)
            return serializer.data
        return None

    # def get_shop_panel_hook(self, obj):
    #     if obj.shop_panel_hooks.exists():
    #         # Filter out non-integer serial_no values
    #         shop_panel_hooks = obj.shop_panel_hooks.filter(
    #             serial_no__regex=r'^\d+$'  # Regex to match only integer values
    #         ).annotate(
    #             serial_no_int=Cast('serial_no', IntegerField())
    #         ).order_by('serial_no_int')
    #         serializer = ShopPanelHookSerializer(shop_panel_hooks, many=True)
    #         return serializer.data
    #     return None

class HookProductCreateUpdateSerializer(serializers.ModelSerializer): 
    product_slug = serializers.CharField()
    shop_panel_hook_slug = serializers.CharField()
    
    class Meta:
        model = ShopPanelHook
        fields = [
                    'product_slug',
                    'shop_panel_hook_slug',
                    'serial_no',
                    'is_active',
                    'remarks',
                ]
    
class HookProductSerializer(serializers.ModelSerializer): 

    class Meta:
        model = ShopPanelHook
        fields = "__all__"