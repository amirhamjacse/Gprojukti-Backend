import base64
import random
from django.conf import settings
from rest_framework import serializers
from base.serializers import CompanyLiteSerializer
from gporjukti_backend_v2.settings import BASE_URL
from product_management.models.category import *
from product_management.models.product import Product
from user.serializers import BaseSerializer
from drf_extra_fields.fields import Base64FileField, Base64ImageField

class CategoryGroupSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    image = Base64ImageField(write_only = True, required=False)
    banner_image = serializers.CharField(read_only = True)
    
    class Meta:
        model = CategoryGroup
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(CategoryGroupSerializer, self).to_representation(instance)
    
    

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    image = Base64ImageField(write_only = True, required=False)
    
    class Meta:
        model = Category
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(CategorySerializer, self).to_representation(instance)

class CategoryLiteSerializer(serializers.ModelSerializer):
    company = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = [
                  'id',
                  'name',
                  'slug',
                  'company'
                  ]
       
    def to_representation(self, instance):
        self.fields["company"] = CompanyLiteSerializer(read_only=True)
        return super(CategoryLiteSerializer, self).to_representation(instance)
    
    
class CategoryWiseProductSerializer(serializers.ModelSerializer): 
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
        image_url = settings.NOT_FOUND_IMAGE
        
        if obj.images:
            image_url = obj.image 
        return image_url
        
class CategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    is_child = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Category
        fields = [
                    'id',
                    'name',
                    'slug',
                    'image',
                    'status',
                    'is_active',
                    'is_featured',
                    'show_in_ecommerce',
                    'is_child',
                ]
    
    def get_is_child(self, obj):
        is_child = False
        
        if obj.status in ["CHILD", "CHILD_OF_CHILD"]:
            is_child = True
        
        return is_child
    
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        
        if obj.image:
            image_url = obj.image 
        return image_url
        
class GroupWiseSubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                    'id',
                    'name',
                    'slug',
                ]
        
        
class GroupWiseCategoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Category
        fields = [
                    'id',
                    'name',
                    'slug',
                    'sub_category',
                ]
        
    def get_sub_category(self, obj):
        qs = Category.objects.filter(category_parent = obj)
        if qs:
            serializer = GroupWiseSubCategoryListSerializer(instance=qs, many = True)
            return serializer.data
        return None
        
class CategoryGroupListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = CategoryGroup
        fields = [
                    'id',
                    'name',
                    'slug',
                    'category',
                ]
        
    def get_category(self, obj):
        if obj.categories:
            serializer = GroupWiseCategoryListSerializer(instance=obj.categories.all(), many = True)
            return serializer.data
        return None
    

class PublicCategoryListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Category
        fields = "__all__"
        
    def get_image(self, obj):
        image_url = settings.NOT_FOUND_IMAGE
        if not obj.image:
            image_url = image_url
        else:
            image_url = obj.image 
            
        return image_url