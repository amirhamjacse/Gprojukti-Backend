import base64
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer
from product_management.models.brand_seller import *
from user.serializers import BaseSerializer
from drf_extra_fields.fields import Base64FileField, Base64ImageField

class BrandListSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    
    class Meta:
        model = Brand
        fields = [
                  'id',
                  'name',
                  'slug',
                  'logo',
                  'is_featured',
                  'is_show_in_ecommece',
                  'is_show_in_pos',
                  'is_active',
                  'remarks'
                  ]
   
class BrandSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    logo = Base64ImageField(required=False)
    
    class Meta:
        model = Brand
        fields = [
                  'id',
                  'name',
                  'slug',
                  'logo',
                  'is_featured',
                  'is_show_in_ecommece',
                  'is_show_in_pos',
                  'is_active',
                  'remarks',
                  'meta_title',
                  'meta_description',
                  'canonical',
                  'created_at',
                  'updated_at',
                  'created_by',
                  'updated_by',
                  ]
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        return super(BrandSerializer, self).to_representation(instance)
    
class BrandDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
                  'id',
                  'name',
                  'slug',
                  'logo',
                  'is_featured',
                  'is_show_in_ecommece',
                  'is_show_in_pos',
                  'is_active',
                  'remarks',
                  'meta_title',
                  'meta_description',
                  'canonical',
                  'created_at',
                  'updated_at',
                  'created_by',
                  'updated_by',
                  ]
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        return super(BrandDetailsSerializer, self).to_representation(instance)
    
   
class SupplierCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    brand = serializers.CharField()
    logo = Base64ImageField(required=False)
    
    class Meta:
        model = Supplier
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        return super(SupplierCreateUpdateSerializer, self).to_representation(instance)
    
class SupplierSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    
    
    class Meta:
        model = Supplier
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["brand"] = BrandListSerializer(read_only=True)
        return super(SupplierSerializer, self).to_representation(instance)
    
    
    
   
class SellerCreateUpdateSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    brand = serializers.CharField()
    logo = Base64ImageField(required=False)
    
    class Meta:
        model = Seller
        fields = [
                'id',  
                'name',  
                'code',  
                'slug',  
                'logo',  
                'registration_no',  
                'phone_number',  
                'type',  
                'website',  
                'address',  
                'contact_person',  
                'brand',  
                'is_active',  
                'remarks',  
                'created_by',  
                'updated_by',  
                ]
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        return super(SellerCreateUpdateSerializer, self).to_representation(instance)
    
class SellerSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    
    
    class Meta:
        model = Seller
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["brand"] = BrandListSerializer(read_only=True)
        return super(SellerSerializer, self).to_representation(instance)
    
    
    