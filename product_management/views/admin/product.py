from typing import Counter
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from human_resource_management.models.employee import EmployeeInformation
from product_management.filter.product import *
from product_management.task.product import *
from product_management.utils import barcode_status_log
from user.models import UserInformation
from utils.actions import activity_log
from utils.decorators import log_activity
from utils.barcode import *
from utils.generates import generate_requisition_no, unique_slug_generator, unique_slug_generator_for_product_category
from utils.response_wrapper import ResponseWrapper

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Sum
from collections import defaultdict
# from django.db.models import Sum

import asyncio
import io
import openpyxl

from django.core.paginator import Paginator
import pandas as pd

from django.http import StreamingHttpResponse
from rest_framework.response import Response
from tablib import Dataset
from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# User = get_user_model()
from rest_framework.permissions import IsAdminUser
from utils.permissions import CheckCustomPermission
# import re
from product_management.models.product import *
from product_management.serializers.product import *

from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from utils.send_sms import send_email
from utils.status_change_log import product_stock_transfer_log
from utils.upload_image import image_upload


from rest_framework.permissions import AllowAny, IsAuthenticated

from io import BytesIO
from openpyxl import Workbook

import asyncio
from asgiref.sync import sync_to_async
import random
# from django.db import transaction

import webcolors

from django.http import HttpResponse
from django.db import connection
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import io

# from django.db.models import F

def closest_color(hex_value):
    min_diff = None
    closest_name = None
    r1, g1, b1 = webcolors.hex_to_rgb(hex_value)
    for name, hex_code in webcolors.CSS3_HEX_TO_NAMES.items():
        r2, g2, b2 = webcolors.hex_to_rgb(hex_code)
        diff = (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2
        if min_diff is None or diff < min_diff:
            min_diff = diff
            closest_name = name
    return closest_name


class ProductAttributeViewSet(CustomViewSet):
    queryset = ProductAttribute.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductAttributeSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductAttributeFilter
    
class ProductAttributeValueViewSet(CustomViewSet):
    queryset = ProductAttributeValue.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductAttributeValueListSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductAttributeValueFilter
    
class ProductViewSet(CustomViewSet):
    queryset = Product.objects.all()
    lookup_field = 'pk'
    serializer_class = ProductDetailsSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductFilter
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = ProductCreateSerializer
        elif self.action in ['bulk_create']:
            self.serializer_class = ProductBulkCreateSerializer
        elif self.action in ['update']:
            self.serializer_class = ProductUpdateSerializer
        elif self.action in ['product_variant_create_update']:
            self.serializer_class = ProductVariantCreateSerializer
        elif self.action in ['product_image_upload', 'product_variant_image_upload']:
            self.serializer_class = Base64ImageListFieldSerializer
        elif self.action in ['list']:
            self.serializer_class = ProductListSerializer
        elif self.action in ['shop_wise_product_list']:
            self.serializer_class = ShopProductListSerializer
        elif self.action in ['product_price_info_create']:
            self.serializer_class = ProductPriceInfoCreateSerializer
        elif self.action in ['product_description_create']:
            self.serializer_class = ProductDescriptionCreateSerializer
        elif self.action in ['product_warranty_create']:
            self.serializer_class = ProductWarrantyCreateSerializer
        elif self.action in ['product_attribute_value_create_update']:
            self.serializer_class = ProductAttributeValueCreateUpdateSerializer
        else:
            self.serializer_class = ProductDetailsSerializer

        return self.serializer_class
    
    def get_filterset_class(self):
        if self.action in ['shop_wise_product_list']:
            self.filterset_class = ShopWiseProductFilter
        else:
            self.filterset_class = ProductFilter

        return self.filterset_class
    
    def get_permissions(self):
        if self.action in ["shop_wise_product_list"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def unique_product_code(self, request, *args, **kwargs):
        product_code = None
        
        while not product_code:
            product_code = random.randint(10000, 99999)
            product_code_qs = Product.objects.filter(product_code=product_code).last()
            if product_code_qs:
                product_code = None
                
        context = {
            'product_code': f"{product_code}"
        }
        return ResponseWrapper(data= context, msg="Success", status=200)
        
    def product_overview_list(self, request, *args, **kwargs):
        context = [
            {
                'msg': "Total Active Product",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total E-Commerce Product",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Gift Product",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Variant Product",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        
        # qs = ProductPriceInfo.objects.filter( 
        #                 product_price_type="POINT_OF_SELL", 
        #                 msp__gt=0)
        
        
        # for product_price_info in qs: 
        #     product_price_qs = ProductPriceInfo.objects.filter( 
        #                 product_price_type="CORPORATE", product__product_code = product_price_info.product.product_code).last()
            
        #     new_msp = product_price_qs.mrp
        #     new_mrp = product_price_qs.msp
            
        #     # msp_value = product_price_info.msp 
            
        #     product_price_info.mrp = new_mrp
        #     product_price_info.msp = new_msp
        #     count = 1 
        #     rest_of = qs.count() - count
        #     print(f"SI = {count}, Total = {qs.count()}, Rest Of ={rest_of}, Name = {product_price_info.product.name}, MSP = {new_msp}, MRP = {new_mrp}")
        #     count +=1
        #     product_price_info.save()

        return ResponseWrapper(data= context, msg="Success", status=200)
    
    @log_activity
    def list(self, request, *args, **kwargs):
        search  = request.GET.get('search')
        
        qs = self.filter_queryset(self.get_queryset()).filter(status__in = ["STANDALONE", "PARENT"]).order_by('-id')
        
        serializer_class = self.get_serializer_class()
        
        if search:
            product_stock_qs = ProductStock.objects.filter(barcode = search).last()
            
            if product_stock_qs:
                
                if not product_stock_qs.product_price_info:
                    return ResponseWrapper(error_msg="Product Price is Not Found", status=404)
                
                qs = Product.objects.filter(slug = product_stock_qs.product_price_info.product.slug)
        
                page_qs = self.paginate_queryset(qs)
                
                serializer = serializer_class(instance=page_qs, many=True)
                paginated_data = self.get_paginated_response(serializer.data)
                
                paginated_data.data['results'][0]['barcode']=product_stock_qs.barcode
                
                return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
            
            else:
                qs = Product.objects.filter(
                    Q(name__icontains = search)
                    | Q(slug__icontains = search)
                    | Q(product_code__icontains = search)
                ).distinct('name', 'product_code')
                page_qs = self.paginate_queryset(qs)
                serializer = serializer_class(instance=page_qs, many=True)

                paginated_data = self.get_paginated_response(serializer.data)
                return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
            
        else:
            page_qs = self.paginate_queryset(qs)
            serializer = serializer_class(instance=page_qs, many=True)

            paginated_data = self.get_paginated_response(serializer.data)
            return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)      
    
    @log_activity
    def shop_product_list(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request.user)
        
        qs = self.filter_queryset(self.get_queryset()).filter(
            is_gift_product=False, 
            product_price_infos__product_stocks__stock_location__slug__in=shop_qs.values_list('slug', flat=True)
        ).order_by('-id').distinct()
        
        print("shop_qs", shop_qs)

        page_qs = self.paginate_queryset(qs)
        serializer = ShopProductListSerializer(instance=page_qs, many=True, context={'request': request})

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

    #shopwise product list with barcode and status
    @log_activity
    def shop_product_list_barcode(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request.user)
        qs = self.filter_queryset(self.get_queryset()).filter(
            is_gift_product=False, 
            product_price_infos__product_stocks__stock_location__slug__in=shop_qs.values_list('slug', flat=True)
        ).order_by('-id').distinct()
        page_qs = self.paginate_queryset(qs)
        serializer = ShopProductListBarcodeSerializer(
            instance=page_qs, many=True, context={'request': request}
            )
        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)


    @log_activity
    def shop_wise_product_list(self, request, *args, **kwargs):
        shop  = request.GET.get('shop') 
        qs = self.filter_queryset(self.get_queryset())
        
        shop_slug = get_user_store_list(request.user).last().slug
        
        search  = request.GET.get('search')
        
        if search:
            product_stock_qs = ProductStock.objects.filter(barcode = search, status='ACTIVE').last()
            if not product_stock_qs:
                return ResponseWrapper(error_msg="Product is Not Found", status=404, error_code = 404)
            
            elif product_stock_qs:
                
                if not product_stock_qs.product_price_info:
                    return ResponseWrapper(error_msg="Product Price is Not Found", status=404, error_code = 404)
                
                elif not product_stock_qs.stock_location.office_type == "STORE":
                    return ResponseWrapper(error_msg=f"This {search}, Barcode is Not Ready For Sell", status=404, error_code = 404)
                
                elif not product_stock_qs.status == "ACTIVE":
                    return ResponseWrapper(error_msg=f"This {search}, Barcode is Not Ready Active, The Barcode Current Status Is {product_stock_qs.get_status_display()}", status=404, error_code = 404)
                
                if shop_slug:
                    if not product_stock_qs.stock_location.slug == shop_slug:
                        return ResponseWrapper(error_msg=f"This {search}, Barcode is Not Available In Your Stock", status=404, error_code = 404)
                
                qs = Product.objects.filter(slug = product_stock_qs.product_price_info.product.slug)
        
                page_qs = self.paginate_queryset(qs)
                
                serializer = ShopProductListSerializer(instance=page_qs, many=True, context={'request': request})
                paginated_data = self.get_paginated_response(serializer.data)
                
                paginated_data.data['results'][0]['barcode']=product_stock_qs.barcode
                
                return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
        
            qs = qs.filter(name__icontains = search)
            
            
        page_qs = self.paginate_queryset(qs)
        serializer = ShopProductListSerializer(instance=page_qs, many=True, context={'request': request})

        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)


    @log_activity
    def shop_product_list_pos(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request.user)
        
        qs = self.filter_queryset(self.get_queryset()).filter(
            is_gift_product=False, 
            product_price_infos__product_stocks__stock_location__slug__in=shop_qs.values_list('slug', flat=True)
        ).order_by('-id').distinct()
        
        print("shop_qs", shop_qs)

        page_qs = self.paginate_queryset(qs)
        serializer = ShopProductListSerializerShop(instance=page_qs, many=True, context={'request': request})

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)


    # ..........***.......... Product Create ..........***..........
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        # images_file = request.data.pop('images_file', None)
        
        selling_tax_category = request.data.pop('selling_tax_category', '')
        buying_tax_category = request.data.pop('buying_tax_category', '')
        sub_category_list = request.data.pop('sub_category', '')
        
        slug = request.data.pop('slug', '')
        
        # brand_qs = None
        # supplier_qs = None
        # seller_qs = None
        # selling_tax_category_qs = None
            
        if serializer.is_valid():
            # path = 'product' 
            
            name = serializer.validated_data.get('name', '')
            # slug = serializer.validated_data.get('slug', '')
            product_code = serializer.validated_data.get('product_code', '')
            sku = serializer.validated_data.get('sku', '')
            product_parent = serializer.validated_data.pop('product_parent', '')
            gift_product = serializer.validated_data.pop('gift_product', '')
            brand = serializer.validated_data.pop('brand', '')
            supplier = serializer.validated_data.pop('supplier', '')
            seller = serializer.validated_data.pop('seller', '')
            selling_tax_category = serializer.validated_data.pop('selling_tax_category', '')
            buying_tax_category = serializer.validated_data.pop('buying_tax_category', '')
            category_list = serializer.validated_data.pop('category', '')
            sub_category_list = serializer.validated_data.pop('sub_category', '')
            
            product_parent_qs = None
            gift_product_qs = None
            selling_tax_category_qs = None
            buying_tax_category_qs = None
            brand_qs = None
            supplier_qs = None
            seller_qs = None
            selling_tax_category_qs = None
        
            product_name_qs = Product.objects.filter(name=name)
            
            if product_name_qs.exists():
                return ResponseWrapper(error_msg="Product Name is Already Found", error_code=400)
            
            if not category_list:
                return ResponseWrapper(error_msg="Category is Not Found", error_code=404)
            
            if product_parent:
                product_parent_qs = Product.objects.filter(slug=product_parent).last()
                if not product_parent_qs:
                    return ResponseWrapper(error_msg="Product Parent is Not Found", error_code=404)
                
            if gift_product:
                gift_product_qs = Product.objects.filter(slug=gift_product).last()
                if not gift_product_qs:
                    return ResponseWrapper(error_msg="Gift Product is Not Found", error_code=404)
            
            if brand:
                brand_qs = Brand.objects.filter(slug=brand).last()
                if not brand_qs:
                    return ResponseWrapper(error_msg="Product Brand is Not Found", error_code=404)
            
            if seller:
                seller_qs = Seller.objects.filter(slug=seller).last()
                if not seller_qs:
                    return ResponseWrapper(error_msg="Product Seller is Not Found", error_code=404)
            
            if supplier:
                supplier_qs = Supplier.objects.filter(slug=supplier).last()
                if not supplier_qs:
                    return ResponseWrapper(error_msg="Supplier is Not Found", error_code=404)
            
            if selling_tax_category:
                selling_tax_category_qs = TaxCategory.objects.filter(slug=selling_tax_category).last()
                if not selling_tax_category_qs:
                    return ResponseWrapper(error_msg="Selling Tax Category is Not Found", error_code=404)
            
            if buying_tax_category:
                buying_tax_category_qs = TaxCategory.objects.filter(slug=buying_tax_category).last()
                if not buying_tax_category_qs:
                    return ResponseWrapper(error_msg="Buying Tax Category is Not Found", error_code=404)
            
            product_slug_qs = self.queryset.filter(slug=slug)
            
            if product_slug_qs.exists():
                return ResponseWrapper(error_msg="Product Slug is Already Found", error_code=400)
            
            product_code_qs = self.queryset.filter(product_code=product_code)
            if product_code_qs.exists():
                return ResponseWrapper(error_msg="Product Code is Already Found", error_code=400)
            
            # product_sku_qs = self.queryset.filter(sku=sku)
            
            # if product_sku_qs.exists():
            #     return ResponseWrapper(error_msg="Product SKU is Already Found", error_code=400)
            
            if slug:
                slug =  unique_slug_generator_for_product_category(name=slug) if name else None
                
            if not slug:
                slug = unique_slug_generator_for_product_category(name=name) if name else None
            
            
            employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            
            # if not employee_qs or not employee_qs.employee_company:
            #     return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
            # company_id = employee_qs.employee_company
            company_id = Company.objects.all().last()
            
            images_file = request.data.pop('images_file', None)
            
            qs = serializer.save(
                created_by=request.user,
                slug=slug,
                company=company_id
            ) 
            if product_parent:
                if not product_parent_qs:
                    return ResponseWrapper(error_msg="Parent Product is Not Found", error_code=400)
                
                elif product_parent_qs.status in ['STANDALONE', 'PARENT']:
                    qs.status = 'CHILD'
                    qs.save()
                    
                    product_parent_qs.status = 'PARENT'
                    product_parent_qs.save()
                
                elif product_parent_qs.status in ['CHILD']:
                    qs.status = 'CHILD_OF_CHILD'
                    qs.save()
                    
                    product_parent_qs.status = 'CHILD'
                    product_parent_qs.save()
                    
            else:
                qs.status = 'STANDALONE'
                qs.save()
                
            
            if product_parent_qs:
                qs.product_parent = product_parent_qs
            if gift_product_qs:
                qs.gift_product = gift_product_qs
                
            qs.brand = brand_qs
            qs.supplier = supplier_qs
            qs.seller = seller_qs

            if selling_tax_category_qs:
                qs.selling_tax_category = selling_tax_category_qs
                
            if buying_tax_category_qs:
                qs.buying_tax_category = buying_tax_category_qs
                
            qs.save()
            
            for category in category_list:
                qs.category.add(category)
                
            if sub_category_list:
                for sub_category in sub_category_list:
                    qs.sub_category.add(sub_category)
                
            activity_log(qs, request, serializer)
            
            serializer = ProductDetailsSerializer(instance=qs)
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
    @log_activity
    def product_image_upload(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,many=True, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        product_image_list = serializer.validated_data
        image_list = []
        
        for product_image in product_image_list:
            image_file = product_image.get('image')
            path = 'product'
            
            if image_file:
                image_link = image_upload(file=image_file, path=path)
                image_list.append(image_link)
                
            else:
                image_link = None
            
        return ResponseWrapper(data=image_list, msg='created', status=200)
        
    @log_activity
    def product_variant_image_upload(self, request, product_slug,*args, **kwargs):
        product_qs = Product.objects.filter(slug= product_slug).last()
        
        if not product_qs:
            return ResponseWrapper(error_msg="Product is Not Found", error_code=404)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,many=True, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        product_image_list = serializer.validated_data
        image_list = []
        
        for product_image in product_image_list:
            image_file = product_image.get('image')
            path = 'product'
            
            if image_file:
                image_link = image_upload(file=image_file, path=path)
                image_list.append(image_link)
                
            else:
                image_link = None
                
        product_qs.images = image_list
        product_qs.save()
            
        return ResponseWrapper(data=image_list, msg='created', status=200)
    
    
    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        # Fetch the existing product using the slug
        product_qs = Product.objects.filter(slug=slug).last()
        
        if not product_qs:
            return ResponseWrapper(error_msg="Product is Not Found", error_code=404)
        
        sub_category = request.data.pop('sub_category', None)
        seller = request.data.pop('seller', None)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            name = validated_data.get('name', product_qs.name)
            product_parent_slug = validated_data.pop('product_parent', None)
            gift_product_slug = validated_data.pop('gift_product', None)
            brand_slug = validated_data.pop('brand', None)
            supplier_slug = validated_data.pop('supplier', None)
            seller_slug = seller
            selling_tax_category_slug = validated_data.pop('selling_tax_category', None)
            buying_tax_category_slug = validated_data.pop('buying_tax_category', None)
            category_list = validated_data.pop('category', product_qs.category.all())
            
            product_parent_qs = None
            gift_product_qs = None
            selling_tax_category_qs = None
            buying_tax_category_qs = None
            brand_qs = None
            supplier_qs = None
            seller_qs = None
            selling_tax_category_qs = None
            
            # Manage sub_category_list
            sub_category_list = sub_category or product_qs.sub_category.all()
            
            # Ensure the new product name does not exist in other products
            if Product.objects.exclude(slug=slug).filter(name=name).exists():
                return ResponseWrapper(error_msg="Product Name is Already Found", error_code=400)
            
            # Helper function to fetch related objects
            def get_related_object(model, slug, error_msg):
                if slug:
                    obj = model.objects.filter(slug=slug).last()
                    if not obj:
                        return ResponseWrapper(error_msg=error_msg, error_code=404)
                    return obj
                return None
            
            product_name_qs = Product.objects.exclude(slug = slug).filter(name=name)
            
            if product_name_qs.exists():
                return ResponseWrapper(error_msg="Product Name is Already Found", error_code=400)
            
            if name:
                product_name = name
                
            elif not name:
                product_name = product_qs.name
            
            product_parent_qs = None
            gift_product_qs = None
            
            print('name', product_name)
            
            if not category_list:
                return ResponseWrapper(error_msg="Category is Not Found", error_code=404)
            
            if product_parent_slug:
                product_parent_qs = Product.objects.filter(slug=product_parent_slug).last()
                if not product_parent_qs:
                    return ResponseWrapper(error_msg="Product Parent is Not Found", error_code=404)
                
            if gift_product_slug:
                gift_product_qs = Product.objects.filter(slug=gift_product_slug).last()
                if not gift_product_qs:
                    return ResponseWrapper(error_msg="Gift Product is Not Found", error_code=404)
            
            if brand_slug:
                brand_qs = Brand.objects.filter(slug=brand_slug).last()
                if not brand_qs:
                    return ResponseWrapper(error_msg="Product Brand is Not Found", error_code=404)
            
            if supplier_slug:
                supplier_qs = Supplier.objects.filter(slug=supplier_slug).last()
                if not supplier_qs:
                    return ResponseWrapper(error_msg="Supplier is Not Found", error_code=404)
                
            if seller_slug:
                seller_qs = Seller.objects.filter(slug=seller_slug).last()
                if not seller_qs:
                    return ResponseWrapper(error_msg="Supplier is Not Found", error_code=404)
            
            if selling_tax_category_slug:
                selling_tax_category_qs = TaxCategory.objects.filter(slug=selling_tax_category_slug).last()
                if not selling_tax_category_qs:
                    return ResponseWrapper(error_msg="Selling Tax Category is Not Found", error_code=404)
            
            if buying_tax_category_slug:
                buying_tax_category_qs = TaxCategory.objects.filter(slug=buying_tax_category_slug).last()
                if not buying_tax_category_qs:
                    return ResponseWrapper(error_msg="Buying Tax Category is Not Found", error_code=404)
            
            if not category_list:
                return ResponseWrapper(error_msg="Category is Not Found", error_code=404)
            
            employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            company_id = Company.objects.all().last()            
            images_file = request.data.pop('images_file', None)
            
            # Update the product instance
            validated_data.update({
                'name': product_name,
                'product_parent': product_parent_qs,
                'gift_product': gift_product_qs,
                'brand': brand_qs,
                'supplier': supplier_qs,
                'selling_tax_category': selling_tax_category_qs,
                'buying_tax_category': buying_tax_category_qs,
                'seller': seller_qs,
            })
            
            qs = serializer.update(instance=product_qs, validated_data=validated_data)
            
            product_qs = Product.objects.filter(slug = qs.slug).last()
            
            slug = unique_slug_generator_for_product_category(name = product_name)
            
            product_qs.name = product_name
            product_qs.slug = slug
            product_qs.brand = brand_qs
            product_qs.supplier = supplier_qs
            product_qs.seller = seller_qs

            if selling_tax_category_qs:
                product_qs.selling_tax_category = selling_tax_category_qs
                
            if buying_tax_category_qs:
                product_qs.buying_tax_category = buying_tax_category_qs
                
            product_qs.save()
            
            
            # Update product status based on product_parent
            if product_parent_slug:
                if product_parent_qs.status in ['STANDALONE', 'PARENT']:
                    product_parent_qs.status = 'PARENT'
                    product_parent_qs.save()
                    qs.status = 'CHILD'
                    qs.save()
                elif product_parent_qs.status == 'CHILD':
                    product_parent_qs.status = 'CHILD'
                    product_parent_qs.save()
                    qs.status = 'CHILD_OF_CHILD'
                    qs.save()
            else:
                qs.status = 'STANDALONE'
                qs.save()
            
            # Update product categories and subcategories
            if category_list:
                for category in category_list:
                    product_qs.category.add(category)
                
            try:
                if sub_category_list:
                    print('ffffffffff', sub_category_list)
                    
                    for sub_category in sub_category_list:
                        product_qs.sub_category.add(sub_category)
                        
            except:
                pass
            
            serializer = ProductDetailsSerializer(instance=qs)
            
            return ResponseWrapper(data=serializer.data, msg='Product updated', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
    
    @log_activity
    def product_attribute_value_create_update(self, request, product_slug, *args, **kwargs):
        serializer_class = self.get_serializer_class() 
        
        serializer = serializer_class(data=request.data, many=True, partial = True)
        
        product_qs = Product.objects.filter(slug = product_slug).last()
        if not product_qs:
            return ResponseWrapper(error_msg='Product is not found', error_code=404)
        
        request_data_list = request.data
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        for item  in request_data_list:
            product_attribute = item.get('product_attribute')
            value = item.get('value') 
            
            product_attribute_qs = ProductAttribute.objects.filter(slug = product_attribute).last()
            if not product_attribute_qs:
                return ResponseWrapper(error_msg='Product Attribute is not found', error_code=404)
            
            slug = unique_slug_generator(name = value) or None
            
            qs = ProductAttributeValue.objects.create(
                product_attribute = product_attribute_qs,
                value = value, 
                slug = slug,
                created_by = request.user
            ) 
            product_qs.product_attribute_value.add(qs) 
            
        serializer = ProductDetailsSerializer(instance=product_qs)
        
        return ResponseWrapper(data=serializer.data, msg='created', status=200)
    
    
    @log_activity
    def product_price_info_create(self, request, product_slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, many=True, partial = True)
        
        product_qs = Product.objects.filter(slug = product_slug).last()
        
        if not product_qs:
            return ResponseWrapper(error_msg='Product is not found', error_code=404)
        
        request_data_list = request.data
        
        # if not serializer.is_valid():
        #     return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        for item  in request_data_list:
            advance_amount_type = "FLAT"
            
            discount = item.get('discount') or None
            promo_code = item.get('promo_code') or None
            
            product_price_type = item.get('product_price_type')
            buying_price = item.get('buying_price') or 0.0
            gsheba_amount = item.get('gsheba_amount') or 0.0
            msp = item.get('msp') or 0.0
            mrp = item.get('mrp') or 0.0 
            advance_amount = item.get('advance_amount') or 0.0 
            
            try:
                if item.get('advance_amount_type'):
                    advance_amount_type = item.get('advance_amount_type')
            except:
                advance_amount_type = advance_amount_type
            
            discount_qs = None
            promo_code_qs = None
            
            if discount:
                discount_qs = Discount.objects.filter(slug = discount).last()
                if not discount_qs:
                    return ResponseWrapper(error_msg='Discount is not found', error_code=404)
            
            if promo_code:
                promo_code_qs = PromoCode.objects.filter(slug = promo_code).last()
                if not promo_code_qs:
                    return ResponseWrapper(error_msg='Promo Code is not found', error_code=404)
               
            product_price_info_qs = ProductPriceInfo.objects.filter(
                product_price_type = product_price_type,
                product = product_qs
            )
            
            if not product_price_info_qs:
                product_price_info_qs = ProductPriceInfo.objects.create(
                    product = product_qs,
                    discount = discount_qs,
                    promo_code = promo_code_qs,
                    product_price_type = product_price_type,
                    buying_price = buying_price,
                    gsheba_amount = gsheba_amount,
                    advance_amount_type = advance_amount_type,
                    msp = msp,
                    mrp = mrp, 
                    advance_amount = advance_amount,
                    created_by = request.user
                )
            else:
                product_price_info_qs.update(
                    discount = discount_qs,
                    promo_code = promo_code_qs,
                    product_price_type = product_price_type,
                    buying_price = buying_price,
                    gsheba_amount = gsheba_amount,
                    advance_amount_type = "FLAT",
                    msp = msp,
                    mrp = mrp, 
                    advance_amount = advance_amount,
                )
            
        serializer = ProductDetailsSerializer(instance=product_qs)
        
        return ResponseWrapper(data=serializer.data, msg='created', status=200)
    
    @log_activity
    def product_description_create(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

        product_qs = Product.objects.filter(slug = slug).last()
        
        if not product_qs:
            return ResponseWrapper(error_msg='Product is not found', error_code=400)
        
        qs = serializer.update(
            instance=product_qs, 
            validated_data=serializer.validated_data)
        
        serializer = ProductDetailsSerializer(qs)
        
        return ResponseWrapper(data=serializer.data, msg='created', status=200)

    @log_activity
    def product_warranty_create(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, many=True)

        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

        product_qs = Product.objects.filter(slug=slug).last()
        if not product_qs:
            return ResponseWrapper(error_msg='Product is not found', error_code=400)

        request_data_list = request.data

        for product_warranty_data in request_data_list:
            warranty_type = product_warranty_data.get('warranty_type')
            value = product_warranty_data.get('value')
            warranty_duration = product_warranty_data.get('warranty_duration')
            is_active = product_warranty_data.get('is_active')
            remarks = product_warranty_data.get('remarks')

            qs = ProductWarranty.objects.filter(
                product__slug=slug, warranty_type=warranty_type
            )

            if not qs:
                qs = ProductWarranty.objects.create(product = product_qs,
                    warranty_type=warranty_type, value=value,
                    warranty_duration=warranty_duration, is_active=is_active,
                    remarks=remarks,
                    created_by=request.user, updated_by=request.user
                )
            else:
                qs = qs.update(
                    warranty_type=warranty_type, value=value,
                    warranty_duration=warranty_duration, is_active=is_active,
                    remarks=remarks,
                    created_by=request.user, updated_by=request.user
                )

        serializer = ProductDetailsSerializer(product_qs)

        return ResponseWrapper(data=serializer.data, msg='created', status=200)
    
    @log_activity
    def product_variant_create_update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        product_qs = Product.objects.filter(slug=slug).last()
        if not product_qs:
            return ResponseWrapper(error_msg='Product is not found', error_code=404)

        product_code = request.data.get('product_code')
        sku = request.data.get('sku')

        if not product_code:
            return ResponseWrapper(error_msg='Product Code not found', error_code=400)

        product_code_qs = Product.objects.filter(product_code=product_code).last()
        if product_code_qs:
            return ResponseWrapper(error_msg='Product Code is already found', error_code=400)

        slug = unique_slug_generator_for_product_category(name=product_qs.name)
        product_attribute_value_list = []

        product_attribute_list = request.data.get('product_attribute')
        product_price_list = request.data.get('product_price')
        
        color_name = ''
        storage_name = ''


        for product_attributes_data in product_attribute_list:
            product_attribute = product_attributes_data.get('product_attribute')
            product_attribute_value = product_attributes_data.get('product_attribute_value')

            product_attribute_qs = ProductAttribute.objects.filter(slug=product_attribute).last()
            if not product_attribute_qs:
                return ResponseWrapper(error_msg='Product Attribute is not found', error_code=404)

            product_attribute_value_qs = ProductAttributeValue.objects.filter(slug=product_attribute_value).last()
            
            if not product_attribute_value_qs:
                slug = unique_slug_generator(name=product_attribute_value) or None
                
                product_attribute_value_qs = ProductAttributeValue.objects.create(
                    product_attribute=product_attribute_qs,
                    value=product_attribute_value,
                    slug=slug,
                    created_by=request.user,
                    updated_by=request.user
                )
            else:
                product_attribute_value_qs.value = product_attribute_value
                product_attribute_value_qs.updated_by = request.user
                product_attribute_value_qs.save()

            product_attribute_value_list.append(product_attribute_value_qs)
            
            if product_attribute == 'color':
                # try:
                #     # Convert hex code to color name
                #     color_name = webcolors.hex_to_name(product_attribute_value)
                # except ValueError:
                #     # If the color name is not found, find the closest color name
                #     color_name = closest_color(product_attribute_value)
                
                color_name = product_attribute_value.replace("#", "")
                
            if product_attribute == 'storage1':
                # try:
                #     # Convert hex code to color name
                #     color_name = webcolors.hex_to_name(product_attribute_value)
                # except ValueError:
                #     # If the color name is not found, find the closest color name
                #     color_name = closest_color(product_attribute_value)
                
                storage_name = product_attribute_value
                    
                    
        new_product_name = product_qs.name
        
        if color_name:
            new_product_name = f"{product_qs.name} (#{color_name} Color)"
            
        product_slug = unique_slug_generator_for_product_category(name=f"{product_qs.name} (With {product_code} Code)")
            
        product_variant_qs = Product.objects.create(
            name=new_product_name,
            slug=product_slug,
            status='CHILD',
            product_parent=product_qs,
            translation=product_qs.translation,
            specifications=product_qs.specifications,
            meta=product_qs.meta,
            short_description=product_qs.short_description,
            description=product_qs.description,
            minimum_stock_quantity=product_qs.minimum_stock_quantity,
            is_featured=product_qs.is_featured,
            is_top_sale=product_qs.is_top_sale,
            is_upcoming=product_qs.is_upcoming,
            is_new_arrival=product_qs.is_new_arrival,
            is_on_the_go=product_qs.is_on_the_go,
            is_out_of_stock=product_qs.is_out_of_stock,
            is_gift_product=product_qs.is_gift_product,
            is_special_day=product_qs.is_special_day,
            show_on_landing_page=product_qs.show_on_landing_page,
            is_active=product_qs.is_active,
            remarks=product_qs.remarks,
            integrity_guaranteed=product_qs.integrity_guaranteed,
            product_code=product_code,
            banner_message=product_qs.banner_message,
            brand=product_qs.brand,
            supplier=product_qs.supplier,
            selling_tax_category=product_qs.selling_tax_category,
            buying_tax_category=product_qs.buying_tax_category,
            company=product_qs.company,
            images=product_qs.images,
            sku=sku,
            video_link=product_qs.video_link,
            meta_title=product_qs.meta_title,
            meta_image=product_qs.meta_image,
            meta_description=product_qs.meta_description,
            og_title=product_qs.og_title,
            og_image=product_qs.og_image,
            og_url=product_qs.og_url,
            og_description=product_qs.og_description,
            canonical=product_qs.canonical,
            created_by=request.user
        )

        for item in product_price_list:
            discount_slug = item.get('discount')
            promo_code_slug = item.get('promo_code')
            product_price_type = item.get('product_price_type')
            buying_price = item.get('buying_price') or 0.0
            gsheba_amount = item.get('gsheba_amount') or 0.0
            msp = item.get('msp') or 0.0
            mrp = item.get('mrp') or 0.0
            advance_amount = item.get('advance_amount') or 0.0

            discount_qs = None
            promo_code_qs = None

            if discount_slug:
                discount_qs = Discount.objects.filter(slug=discount_slug).last()
                if not discount_qs:
                    return ResponseWrapper(error_msg='Discount is not found', error_code=404)

            if promo_code_slug:
                promo_code_qs = PromoCode.objects.filter(slug=promo_code_slug).last()
                if not promo_code_qs:
                    return ResponseWrapper(error_msg='Promo Code is not found', error_code=404)

            product_price_info_qs = ProductPriceInfo.objects.filter(
                product_price_type=product_price_type,
                product=product_variant_qs
            ).first()

            if not product_price_info_qs:
                product_price_info_qs = ProductPriceInfo.objects.create(
                    product=product_variant_qs,
                    discount=discount_qs,
                    promo_code=promo_code_qs,
                    product_price_type=product_price_type,
                    buying_price=buying_price,
                    gsheba_amount=gsheba_amount,
                    msp=msp,
                    mrp=mrp,
                    advance_amount=advance_amount,
                    created_by=request.user
                )
            else:
                product_price_info_qs.update(
                    discount=discount_qs,
                    promo_code=promo_code_qs,
                    product_price_type=product_price_type,
                    buying_price=buying_price,
                    gsheba_amount=gsheba_amount,
                    msp=msp,
                    mrp=mrp,
                    advance_amount=advance_amount,
                    advance_amount_type = "FLAT",
                )

        for product_attribute_value in product_attribute_value_list:
            product_variant_qs.product_attribute_value.add(product_attribute_value)

        try:
            for category in product_qs.category.all():
                product_variant_qs.category.add(category)
            for sub_category in product_qs.sub_category.all():
                product_variant_qs.sub_category.add(sub_category)
        except:
            pass

        serializer = ProductDetailsSerializer(product_qs)
        return ResponseWrapper(data=serializer.data, msg='created', status=200)    
    
class ProductStockViewSet(CustomViewSet):
    queryset = ProductStock.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = ProductStockSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductStockFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = ProductStockCreateUpdateSerializer
        elif self.action in ['single_barcode_print', 'multiple_barcode_print']:
            self.serializer_class = BarcodePrintSerializer
        elif self.action in ['same_barcode_in_single_page', 'same_barcode_print']:
            self.serializer_class = SameBarcodePrintSerializer
        elif self.action in ['list']:
            self.serializer_class = ProductStockListSerializer
        else:
            self.serializer_class = ProductStockSerializer

        return self.serializer_class
    
    def get_permissions(self):
        # if self.action in ["list"]:
        #     permission_classes = [
        #             (CheckCustomPermission("can_view_list_product_stock"))
        #         ]
        if self.action in ["create",]:
            permission_classes = [IsAuthenticated]
            
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 
    
        # ..........***.......... Get All Data ..........***..........
        
    @log_activity
    def list(self, request, *args, **kwargs):
        employee_qs = EmployeeInformation.objects.filter(work_station__name__icontains = "GProjukti.com - Warehouse", user__email=request.user.email)

        store_qs = get_user_store_list(request_user = request.user)
        
        if employee_qs:
            qs = self.filter_queryset(self.get_queryset()).filter(stock_location__slug__in = store_qs.values_list('slug', flat=True), stock_location__name__icontains = "GProjukti.com - Warehouse")
        else:
            qs = self.filter_queryset(self.get_queryset()).filter(stock_location__slug__in = store_qs.values_list('slug', flat=True))
        
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
        
    @log_activity
    def product_wise_inventory_list(self, request, product_slug,  *args, **kwargs):
        store_qs = get_user_store_list(request_user = request.user)
        
        product_qs =  Product.objects.filter(slug = product_slug).last()
        
        if not product_qs:
            return ResponseWrapper(error_msg=f"{product_slug}, is Not Found", error_code=404, status=404)
        
        # employee_qs = EmployeeInformation.objects.filter(work_station__name__icontains = "GProjukti.com - Warehouse", user__email=request.user.email)
        
        # if employee_qs:
        #     qs = self.filter_queryset(self.get_queryset()).filter(stock_location__slug__in = store_qs.values_list('slug', flat=True), stock_location__name__icontains = "GProjukti.com - Warehouse")
        # else:
        #     qs = self.filter_queryset(self.get_queryset()).filter(stock_location__slug__in = store_qs.values_list('slug', flat=True))
        
        print('grrrrrrrrrrrr', store_qs)
            
        qs = self.filter_queryset(self.get_queryset()).filter(product_price_info__product__slug = product_qs.slug, stock_location__slug__in = store_qs.values_list('slug', flat=True))
        
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = ProductStockListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)


    def stock_summary(self, request, product_slug, *args, **kwargs):
        status_stock_list = []

        # Find the product based on slug
        product_qs = Product.objects.filter(slug=product_slug).last()
        if not product_qs:
            return ResponseWrapper(error_msg="Product is Not Found", error_code=404, status=404)

        # Get the user's store list
        shop_qs = get_user_store_list(request.user)
        if not shop_qs:
            return ResponseWrapper(data={}, msg="No store found for user", status=404)

        # Filter the stock queryset based on the store and product slug
        stock_qs = self.filter_queryset(self.get_queryset()).filter(
            stock_location__in=shop_qs,
            product_price_info__product__slug=product_qs.slug
        )

        # Get distinct status values from the stock queryset using a set to ensure uniqueness
        all_barcode_status_list = set(stock_qs.values_list('status', flat=True).distinct())

        # Create a summary list for each status
        for barcode_status in all_barcode_status_list:
            print('barcode_status', barcode_status)
            
            qs = stock_qs.filter(status=barcode_status)
            if qs.exists():
                message = f'Total {qs.last().get_status_display()} Stock'
                total_stock = qs.count()
                total_stock_rating = 0
                
                if stock_qs.count() > 0:
                    total_stock_rating = (total_stock / stock_qs.count()) * 100

                context = {
                    'message': message,
                    'total_stock': total_stock,
                    'total_stock_rating': round(total_stock_rating, 2),
                }
                status_stock_list.append(context)

        response_context = {
            'status_stock': status_stock_list,
        }

        return ResponseWrapper(data=response_context, msg="success", status=200)
    
    def stock_summary_report(self, request, *args, **kwargs):
        status_stock_list = []
        response_context = []
        
        search = request.GET.get('search')

        # Find the product based on slug
        product_qs = Product.objects.filter(product_code = "56469"
                ).order_by('?').last()
        
        if search:
            product_qs = Product.objects.filter(
                Q(name__icontains = search)
                | Q(slug=search)
                | Q(product_code=search)
                ).last()
          
            
        if not product_qs:
            return ResponseWrapper(error_msg="Product is Not Found", error_code=404, status=404)

        # Get the user's store list
        shop_qs = OfficeLocation.objects.filter(office_type__in = ["STORE", "WAREHOUSE"]).order_by("pos_area_name")
        
        if not shop_qs:
            return ResponseWrapper(data={}, msg="No store found for user", status=404)

        # Filter the stock queryset based on the store and product slug
        
        stock_qs = self.filter_queryset(self.get_queryset()).filter(
            product_price_info__product__slug = product_qs.slug
        ).exclude(status__in  = ["SOLD", "IN_TRANSIT", "IN_REQUISITION", "IN_TRANSFER"])
        
        # stock_qs = ProductStock.objects.exclude(status__in  = ["SOLD", "IN_TRANSIT", "IN_REQUISITION", "IN_TRANSFER"]).filter(is_active = True)

        # Get distinct status values from the stock queryset using a set to ensure uniqueness
        all_barcode_status_list = set(stock_qs.values_list('status', flat=True).distinct())

        # Create a summary list for each status
        
        barcode_count = '-'
        
        for shop in shop_qs:
            
            qs = stock_qs.filter(stock_location =  shop)
            
            status_count_qs = qs.values('status').annotate(count=Count('status'))
            
            
            status_msg = []
            if qs.count() > 0:
                for status_count in status_count_qs:
                    
                    status_msg.append((f"Status: {status_count['status']}, Count: {status_count['count']}"))
                
                barcode_count = str(status_msg)
            
            # if qs.exists():
            message = f'POS Area = {shop.pos_area_name}, Shop Name = {shop.name} & Product Code {product_qs.product_code}'
            total_stock = qs.count()
            total_stock_rating = 0
            if stock_qs.count() >0:
                total_stock_rating = (total_stock / stock_qs.count()) * 100
            # barcode_count = f"Active 16"
            
            context = {
                'msg': message,
                'quantity': total_stock,
                'ratio': round(total_stock_rating, 2),
                'others': barcode_count,
            }
            status_stock_list.append(context)


        return ResponseWrapper(data=status_stock_list, msg="success", status=200)
    
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        request_data_list = request.data
        
        for product in request_data_list:
            
            barcode = product.get('barcode')
            if not barcode:
                return ResponseWrapper(error_code=404, error_msg='Barcode is Required')
            barcode_qs = ProductStock.objects.filter(barcode = barcode).last()
            
            if barcode_qs:
                return ResponseWrapper(error_code=404,status=400, error_msg=f'This {barcode} Barcode is Already Exists')
            
            product_code = barcode.split('-')[0]
            
            if not product_code:
                return ResponseWrapper(error_code=404, error_msg='Product Not Found')
            
            product_qs = Product.objects.filter(product_code = product_code).last()
            if not product_qs:
                return ResponseWrapper(error_code=404, error_msg='Product Not Found')
            
            product_price_info_qs = ProductPriceInfo.objects.filter(product__product_code= product_code).last()
            
            if not product_price_info_qs:
                return ResponseWrapper(error_code=404, error_msg='Product Price is Not Found')
            
            today = timezone.now()
            
            remarks = product.get('remarks')
            status = product.get('status')
            is_active = product.get('is_active')
            stock_location = product.get('stock_location')
            stock_location_qs = OfficeLocation.objects.filter(
                slug = stock_location
            ).last()
            if not stock_location_qs:
                return ResponseWrapper(error_code=400, error_msg='Stock Location is Not Found')
            
            qs = ProductStock.objects.create(
                    created_by=request.user,
                    product_price_info = product_price_info_qs,
                    stock_in_date=today,
                    barcode = barcode, 
                    status = status,
                    remarks = remarks,
                    is_active = is_active
            )
            qs.stock_location = stock_location_qs
            qs.save()
            
            if qs:
                product_stock_serializer_data = ProductStockSerializer(qs).data
                
                current_status_display  = product_stock_serializer_data.get('status_display')
                stock_status_change_by_info  = product_stock_serializer_data.get('created_by')
                
                stock_in_age  = product_stock_serializer_data.get('stock_in_age')
                
                stock_location_info  = product_stock_serializer_data.get('stock_location')
                
                product_stock_log_qs = barcode_status_log(product_stock_qs = qs, previous_status = '-', previous_status_display ='-'  , current_status = qs.status, remarks = qs.remarks, is_active = qs.is_active, request_user = request.user,stock_in_date = today)
                
                # product_stock_log_qs = ProductStockLog.objects.create(
                #     product_stock = qs, 
                #     current_status = qs.status,
                #     current_status_display = current_status_display,
                #     remarks = qs.remarks,
                #     is_active = qs.is_active,
                #     stock_status_change_by_info = stock_status_change_by_info,
                #     stock_location_info = stock_location_info,
                #     created_by = request.user,
                #     updated_by = request.user,
                #     stock_in_date = today,
                # )
                #TODO Store info serializer add

        activity_log(qs, request,serializer)
            
        return ResponseWrapper(data=serializer.data, msg='created', status=200)
            
    @log_activity
    def update(self, request, barcode, *args, **kwargs):
        barcode_qs = ProductStock.objects.filter(barcode = barcode).last()
        
        if not barcode_qs:
            return ResponseWrapper(error_code=400, error_msg='Barcode is Not Found')
        
        product_barcode_qs = ProductStock.objects.exclude(
            id = barcode_qs.id).filter(barcode = barcode).last()
        
        if product_barcode_qs:
            return ResponseWrapper(error_code=400, error_msg='Barcode is Already Exist')
        
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        
        previous_product_stock_serializer_data = ProductStockSerializer(barcode_qs).data
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        status = request.data.get('status')
        if status:
            if status == barcode_qs.status:
                serializer = ProductStockSerializer(barcode_qs)
                return ResponseWrapper(data=serializer.data, msg='Barcode Status is Same', status=200)
            
        today = timezone.now()
        
        qs = serializer.update(instance=barcode_qs, validated_data=serializer.validated_data)
        
        if qs:
            product_stock_serializer_data = ProductStockSerializer(qs).data
            
            previous_status_display  = previous_product_stock_serializer_data.get('status_display')
            stock_status_change_by_info  = product_stock_serializer_data.get('created_by')
            
            stock_in_age  = product_stock_serializer_data.get('stock_in_age')
            current_status_display  = product_stock_serializer_data.get('status_display')
            stock_status_change_by_info  = product_stock_serializer_data.get('created_by')
            
            stock_location_info  = product_stock_serializer_data.get('stock_location')

            product_stock_log_qs = ProductStockLog.objects.create(
                product_stock = qs, 
                previous_status = barcode_qs.status,
                previous_status_display = previous_status_display,
                current_status = qs.status,
                current_status_display = current_status_display,
                remarks = qs.remarks,
                is_active = qs.is_active,
                stock_status_change_by_info = stock_status_change_by_info,
                stock_in_date = today,
                stock_in_age = stock_in_age,
                stock_location_info = stock_location_info,
                
                created_by = request.user,
                updated_by = request.user,
            )
            
            #TODO Store info serializer add
            
        serializer = ProductStockSerializer(qs)

        activity_log(qs, request, serializer)

        return ResponseWrapper(data=serializer.data, msg='created', status=200)

    @log_activity
    def retrieve(self, request, barcode, *args, **kwargs):
        barcode_qs = ProductStock.objects.filter(barcode = barcode).last()
        
        if not barcode_qs:
            return ResponseWrapper(error_code=400, error_msg='Barcode is Not Found')
        
        serializer = ProductStockSerializer(barcode_qs)
            
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
                    
    @log_activity      
    def single_barcode_print(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
        data_list = request.data

        response = generate_single_line_barcode_for_pos(data_list)
        
        return response
    
    @log_activity
    def multiple_barcode_print(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
        data_list = request.data

        response = generate_multiple_line_barcode_for_pos(data_list)
        
        return response    
    
    @log_activity
    def same_barcode_in_single_page(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
        data_list = request.data

        response = generate_same_barcode_for_pos(data_list)
        
        return response    
    
    @log_activity
    def same_barcode_print(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
        data_list = request.data

        response = generate_multiple_same_barcode_for_pos(data_list)
        
        return response

class ProductStockWithProductDownloadViewSet(CustomViewSet):
    queryset = ProductStock.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = ProductStockSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductStockFilter
    
    def get_permissions(self):
        if self.action in ["product_stock_list"]:
            permission_classes = [
                    (CheckCustomPermission("can_view_list_product_stock"))
                ]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @staticmethod
    async def generate_excel(serializer_data):
        df = pd.DataFrame(serializer_data)
        stream = io.BytesIO()
        df.to_excel(stream, index=False)
        stream.seek(0)
        return stream.getvalue()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @log_activity
    def list(self, request, product_slug, *args, **kwargs):
        # Get filter parameters from request
        search = request.GET.get('search')
        start_date = request.GET.get('stock_in_start_date')
        end_date = request.GET.get('stock_in_end_date')
        supplier = request.GET.get('supplier')
        seller = request.GET.get('seller')
        officelocation = request.GET.get('stock_location')
        brand = request.GET.get('brand')
        status = request.GET.get('status')
        product_slug = product_slug

        # Construct SQL query to fetch required fields from ProductStock model
        sql_query = """
            SELECT
                ROW_NUMBER() OVER () AS "SI",
                prd.name AS "Product Name",
                prd.product_code AS "Product Code",
                COALESCE(prp.name, '-') AS "Parent Product Name",
                COALESCE(prp.product_code, '-') AS "Parent Product Code",
                br.name AS "Brand",
                sel.name AS "Seller",
                sup.name AS "Supplier",
                ps.barcode AS "Barcode",
                INITCAP(REPLACE(LOWER(ps.status), '_', ' ')) AS "Status",
                psi.msp AS "MSP",
                psi.mrp AS "MRP",
                ps.stock_in_date AS "Stock In Date",
                ps.stock_in_age AS "Stock in Age",
                stlc.name AS "Shop Location"
            FROM
                product_management_productstock ps
            LEFT JOIN
                product_management_productpriceinfo psi ON ps.product_price_info_id = psi.id
            LEFT JOIN
                product_management_product prd ON psi.product_id = prd.id
            LEFT JOIN
                location_officelocation stlc ON ps.stock_location_id = stlc.id
            LEFT JOIN
                product_management_product prps ON psi.product_id = prps.id
            LEFT JOIN
                product_management_supplier sup ON psi.product_id = sup.id
            LEFT JOIN
                product_management_brand br ON prd.brand_id = br.id
            LEFT JOIN
                product_management_seller sel ON prd.brand_id = sel.id
            LEFT JOIN
                product_management_product prp ON prd.product_parent_id = prp.id
            WHERE 1=1
        """

        # Add filters to the SQL query
        print("product_slug = ", product_slug)
        
        if product_slug:
            sql_query += """
                AND (
                    prd.slug ILIKE %(product_slug)s
                )
            """

        if search:
            sql_query += """
                AND (
                    ps.barcode ILIKE %(search)s
                    OR prd.name ILIKE %(search)s
                    OR prd.slug ILIKE %(search)s
                    OR prd.product_code ILIKE %(search)s
                )
            """

        if start_date:
            start_date = datetime.strptime(start_date, '%m-%d-%Y')
        if end_date:
            end_date = datetime.strptime(end_date, '%m-%d-%Y')

        # Calculate the difference in days
        
        # Check if the date range is greater than 31 days
        if start_date and end_date:
            
            date_diff = (end_date - start_date).days
            
            print('date_diff', date_diff)

            if date_diff > 31:
                pass
                # data = {'message': 'Success'}
                # # return Response({'error_msg': 'Date range should not be more than 31 days'}, status=400)
                # return Response(data, status=200)
            
            else:
                sql_query += " AND ps.stock_in_date BETWEEN %(start_date)s AND %(end_date)s"

        if status:
            sql_query += " AND ps.status = %(status)s"
            
        if supplier:
            sql_query += """
                AND (
                    sup.name ILIKE %(supplier)s
                    OR sup.slug ILIKE %(supplier)s
                )
            """
        if brand:
            sql_query += """
                AND (
                    br.name ILIKE %(brand)s
                    OR br.slug ILIKE %(brand)s
                )
            """
        if officelocation:
            sql_query += """
                AND (
                    stlc.name ILIKE %(officelocation)s
                    OR stlc.slug ILIKE %(officelocation)s
                )
            """
        if seller:
            sql_query += """
                AND (
                    sel.name ILIKE %(seller)s
                    OR sel.slug ILIKE %(seller)s
                )
            """

        # Prepare query parameters
        query_params = {
            'product_slug': f'%{product_slug}%' if product_slug else None,
            'search': f'%{search}%' if search else None,
            'start_date': start_date,
            'end_date': end_date,
            'status': status,
            'officelocation': officelocation,
            'seller': seller,
            'supplier': f'%{supplier}%' if supplier else None,
            'brand': f'%{brand}%' if brand else None,
        }

        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, query_params)
            rows = cursor.fetchall()

        # Convert query result into DataFrame
        df = pd.DataFrame(rows, columns=[
            'SI', 'Product Name', 'Product Code', 'Parent Product Name', 'Parent Product Code', 'Brand', 'Seller', 'Supplier', 'Barcode', 'Status', 'MSP', 'MRP', 'Stock In Date', 'Stock in Age', 'Shop Location'])

        # Convert datetime columns to string format for Excel compatibility
        if not df['Stock In Date'].isnull().all():
            df['Stock In Date'] = df['Stock In Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Generate Excel file asynchronously (if needed)
        excel_content = async_to_sync(self.generate_excel)(df)

        # Set filename with today's date
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"Product Stock - {today}.xlsx"

        # Create the HttpResponse object with the appropriate XLSX content-type and headers
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class ProductStockDownloadViewSet(CustomViewSet):
    queryset = ProductStock.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = ProductStockSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductStockFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @staticmethod
    async def generate_excel(serializer_data):
        df = pd.DataFrame(serializer_data)
        stream = io.BytesIO()
        df.to_excel(stream, index=False)
        stream.seek(0)
        return stream.getvalue()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @log_activity
    def list(self, request, *args, **kwargs):
        # Get filter parameters from request
        search = request.GET.get('search')
        start_date = request.GET.get('stock_in_start_date')
        end_date = request.GET.get('stock_in_end_date')
        supplier = request.GET.get('supplier')
        seller = request.GET.get('seller')
        officelocation = request.GET.get('stock_location')
        brand = request.GET.get('brand')
        status = request.GET.get('status')
        is_for_all = request.GET.get('is_for_all')

        # Initialize SQL query
        sql_query = """
            SELECT
                ROW_NUMBER() OVER () AS "SI",
                prd.name AS "Product Name",
                prd.product_code AS "Product Code",
                COALESCE(prp.name, '-') AS "Parent Product Name",
                COALESCE(prp.product_code, '-') AS "Parent Product Code",
                br.name AS "Brand",
                COALESCE(sel.name, '-') AS "Seller",
                COALESCE(sup.name, '-') AS "Supplier",
                psi.msp AS "MSP",
                psi.mrp AS "MRP",
                stlc.name AS "Shop Location"
        """
        
        # sql_query += " FROM product_stock ps" \
        #         " LEFT JOIN product prd ON ps.product_id = prd.id" \
        #         " LEFT JOIN product prp ON prd.parent_product_id = prp.id" \
        #         " LEFT JOIN brand br ON prd.brand_id = br.id" \
        #         " LEFT JOIN seller sel ON ps.seller_id = sel.id" \
        #         " LEFT JOIN supplier sup ON ps.supplier_id = sup.id" \
        #         " LEFT JOIN shop_location stlc ON ps.shop_location_id = stlc.id" \
        #         " WHERE ps.status NOT IN ('SOLD', 'OTHERS')"
    

        # Add conditional aggregations
        
        if is_for_all == "True":
            sql_query += """
                , STRING_AGG(
                    DISTINCT INITCAP(REPLACE(LOWER(ps.status), '_', ' ')),
                    ', '
                ) FILTER (WHERE ps.status NOT IN ('SOLD', 'OTHERS')) AS "Statuses",
                STRING_AGG(
                    DISTINCT ps.barcode,
                    ', '
                ) FILTER (WHERE ps.status NOT IN ('SOLD', 'OTHERS')) AS "Barcodes",
                COUNT(ps.barcode) FILTER (WHERE ps.status NOT IN ('SOLD', 'OTHERS')) AS "Barcode Count"
            """
        else:
            sql_query += """
                , STRING_AGG(
                    DISTINCT INITCAP(REPLACE(LOWER(ps.status), '_', ' ')),
                    ', '
                ) FILTER (WHERE ps.status IN ('ACTIVE', 'GSHEBA_FAULTY', 'COMPANY_WARRANTY_FAULTY', 'SERVICE_WARRANTY_FAULTY')) AS "Statuses",
                STRING_AGG(
                    DISTINCT ps.barcode,
                    ', '
                ) FILTER (WHERE ps.status IN ('ACTIVE', 'GSHEBA_FAULTY', 'COMPANY_WARRANTY_FAULTY', 'SERVICE_WARRANTY_FAULTY')) AS "Barcodes",
                COUNT(ps.barcode) FILTER (WHERE ps.status IN ('ACTIVE', 'GSHEBA_FAULTY', 'COMPANY_WARRANTY_FAULTY', 'SERVICE_WARRANTY_FAULTY')) AS "Barcode Count"
            """

        # Finalize SQL query
        sql_query += """
            FROM
                product_management_productstock ps
            LEFT JOIN
                product_management_productpriceinfo psi ON ps.product_price_info_id = psi.id
            LEFT JOIN
                product_management_product prd ON psi.product_id = prd.id
            LEFT JOIN
                location_officelocation stlc ON ps.stock_location_id = stlc.id
            LEFT JOIN
                product_management_supplier sup ON prd.supplier_id = sup.id
            LEFT JOIN
                product_management_brand br ON prd.brand_id = br.id
            LEFT JOIN
                product_management_seller sel ON prd.seller_id = sel.id
            LEFT JOIN
                product_management_product prp ON prd.product_parent_id = prp.id
            WHERE 1=1
                AND stlc.name IS NOT NULL
                AND stlc.name <> 'Test Shop'
        """

        # Add filters to the SQL query
        if search:
            sql_query += """
                AND (
                    ps.barcode ILIKE %(search)s
                    OR prd.name ILIKE %(search)s
                    OR prd.slug ILIKE %(search)s
                    OR prd.product_code ILIKE %(search)s
                )
            """

        if start_date:
            start_date = datetime.strptime(start_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            sql_query += " AND ps.stock_in_date >= %(start_date)s"

        if end_date:
            end_date = datetime.strptime(end_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            sql_query += " AND ps.stock_in_date <= %(end_date)s"

        if status:
            sql_query += " AND ps.status = %(status)s"

        if supplier:
            sql_query += """
                AND (
                    sup.name ILIKE %(supplier)s
                    OR sup.slug ILIKE %(supplier)s
                )
            """

        if brand:
            sql_query += """
                AND (
                    br.name ILIKE %(brand)s
                    OR br.slug ILIKE %(brand)s
                )
            """

        if officelocation:
            sql_query += """
                AND (
                    stlc.name ILIKE %(officelocation)s
                    OR stlc.slug ILIKE %(officelocation)s
                )
            """

        if seller:
            sql_query += """
                AND (
                    sel.name ILIKE %(seller)s
                    OR sel.slug ILIKE %(seller)s
                )
            """

        # Group by relevant columns
        sql_query += """
            GROUP BY
                prd.name, prd.product_code, prp.name, prp.product_code, br.name,
                sup.name, psi.msp, psi.mrp, stlc.name, sel.name
        """

        # Order by product code
        sql_query += """
            ORDER BY
                prd.product_code
        """

        # Prepare query parameters
        query_params = {
            'search': f'%{search}%' if search else None,
            'start_date': start_date,
            'end_date': end_date,
            'supplier': f'%{supplier}%' if supplier else None,
            'brand': f'%{brand}%' if brand else None,
            'officelocation': f'%{officelocation}%' if officelocation else None,
            'seller': f'%{seller}%' if seller else None,
            'status': status if status else None
        }

        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql_query, query_params)
            rows = cursor.fetchall()

        # Convert query result into DataFrame
        df = pd.DataFrame(rows, columns=[
            'SI', 'Product Name', 'Product Code', 'Parent Product Name', 'Parent Product Code', 'Brand',
            'Seller', 'Supplier', 'MSP', 'MRP', 'Shop Location', 'Statuses', 'Barcodes', 'Barcode Count',
        ])

        # Generate Excel file asynchronously (if needed)
        excel_content = async_to_sync(self.generate_excel)(df)

        # Set filename with today's date
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"Product Stock - {today}.xlsx"

        # Create the HttpResponse object with the appropriate XLSX content-type and headers
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response



class ProductStockTransferViewSet(CustomViewSet):
    queryset = ProductStockTransfer.objects.all().order_by('-created_at')
    lookup_field = 'pk'
    serializer_class = ProductStockTransferSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductStockTransferFilter
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = ProductStockTransferCreateSerializer
        elif self.action in ['product_stock_transfer_received']:
            self.serializer_class = ProductStockTransferReceivedSerializer
        elif self.action in ['update']:
            self.serializer_class = ProductStockTransferUpdateSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = ProductStockTransferSerializer
        elif self.action in ['list']:
            self.serializer_class = ProductStockTransferListSerializer
        else:
            self.serializer_class = ProductStockTransferSerializer

        return self.serializer_class
    # ..........***.......... Get All Data ..........***..........
    
    @log_activity
    def list(self, request, *args, **kwargs):
        store_list_qs =  get_user_store_list(request_user = request.user)
        
        store_slug_list = store_list_qs.values_list('slug', flat = True)
        
        
        user_qs = UserInformation.objects.filter(user = request.user).last()
        
        qs = self.filter_queryset(self.get_queryset()).filter(
                Q(from_shop__slug__in = store_slug_list)
                | Q(to_shop__slug__in = store_slug_list)
                )
        
        try:
            if user_qs and user_qs.user_type.name in ["Shop"]:
                qs = qs.filter(to_shop__slug__in=store_slug_list)
            else:
                pass
        except AttributeError:
            # Handle the case where user_qs or user_qs.user_type is None or has no 'name' attribute
            pass
        
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        from_shop = request.data.get('from_shop')
        to_shop = request.data.get('to_shop')
        
        product_stock_list = request.data.get('product_stock')
        
        if not product_stock_list:
            return  ResponseWrapper(error_msg='Barcode List is Not Given', error_code=400)
        
        from_shop_qs = OfficeLocation.objects.filter(slug = from_shop).last()
        to_shop_qs = OfficeLocation.objects.filter(slug = to_shop).last()
        
        if not from_shop_qs:
            return  ResponseWrapper(error_msg='From Shop is Not Found', error_code=400)
        if not to_shop_qs:
            return  ResponseWrapper(error_msg='Destination Shop is Not Found', error_code=400)
        
        if from_shop_qs == to_shop_qs:
            return  ResponseWrapper(error_msg='From Shop and Destination Shop is Same', error_code=400)
        
        
        all_barcode = set(product_stock_list)
        product_stock_qs = ProductStock.objects.filter(barcode__in=product_stock_list)
        found_barcode = set(product_stock_qs.values_list('barcode', flat=True))
        
        not_found_barcode = all_barcode - found_barcode
        
        if not_found_barcode:
            return ResponseWrapper(error_msg=f'This {", ".join(not_found_barcode)}, Barcode is Not Found', error_code=400)
        
        # Check that all product stocks are located in the from_shop
        product_stock_in_from_shop_qs = ProductStock.objects.filter(
            barcode__in=product_stock_list,
            stock_location = from_shop_qs
        )
        
        print(f"Stock_location = {product_stock_qs.last().stock_location}, {product_stock_qs.last()}")
        
        found_barcode_in_from_shop = set(product_stock_in_from_shop_qs.values_list('barcode', flat=True))
        
        not_found_barcode_in_from_shop = all_barcode - found_barcode_in_from_shop
        
        if not_found_barcode_in_from_shop:
            return ResponseWrapper(error_msg=f'Not all Barcode(s) are Found in "{from_shop_qs.name}": {", ".join(not_found_barcode_in_from_shop)}', error_code=400)
        
        
        last_stock_transfer_qs = ProductStockTransfer.objects.all().order_by('id').last()
        
        if last_stock_transfer_qs:
            last_requisition_no = last_stock_transfer_qs.requisition_no
        else:
            last_requisition_no = "REG00000001"
            
        requisition_no = generate_requisition_no(last_requisition_no = last_requisition_no)
        
        approved_by_qs = EmployeeInformation.objects.filter(user__id = request.user.id).last() 
        
        product_stock = serializer.validated_data.pop('product_stock', None)
        
        product_stock_transfer_qs = ProductStockTransfer.objects.filter(product_stock__barcode__in = product_stock_list, status__in = ['IN_TRANSIT', 'UPDATED']).last()
        
        if product_stock_transfer_qs:
            return ResponseWrapper(error_msg=f'Products is Already In a Stock Transfer, which is #{product_stock_transfer_qs.requisition_no} and the status is {product_stock_transfer_qs.get_status_display()}', error_code=400)
        
        qs = serializer.save(
                requisition_no=requisition_no,
                created_by=request.user,
                from_shop=from_shop_qs,
                to_shop=to_shop_qs,
                approved_by = approved_by_qs
            )
        # qs.product_stock.add(product_stock)
        
        for barcode in product_stock_list:
            product_stock_qs = ProductStock.objects.filter(barcode = barcode).last()
            if qs.stock_transfer_type == 'TRANSFER':
                if product_stock_qs:
                    product_stock_qs.status = 'IN_TRANSFER'
                
                    qs.product_stock.add(product_stock_qs)
                    product_stock_qs.save()
            
        serializer = ProductStockTransferSerializer(instance=qs)
        
        
        
        status_change_reason = f"An Stock Transfer is Created By '{request.user.first_name} {request.user.last_name}', And  The Transfer number is  = #{requisition_no} at {qs.created_at}"
        
        if qs:
            product_stock_transfer_log(product_stock_transfer_qs= qs, request_user= request.user, status_change_reason=status_change_reason)
            
        try:
            subject = f"Stock Transfer Request From {from_shop_qs.name} to {to_shop_qs.name}"
            
            message_body = f"<html><p> Dear Concern, </strong> <br> Please verify that your panel is 'https://admin.grprojukti.com/stock-transfer/'. A stock transfer request create on behalf of <strong>'{from_shop_qs.name} to {to_shop_qs.name}' </strong>, for your approval and the stock transfer number is <strong> {requisition_no} </strong>.</p>Thank you, <br> G-Projukti.com </html>"

            ware_house = from_shop_qs.office_type
            # change with actual email address
            if ware_house == 'WAREHOUSE':
                mail_address = 'haider.chowdhury@gprojukti.com'
                send_email(email=mail_address, subject= subject, body=message_body)
            else:
                print("else condition in mail")
                # mail_address = 'razib.shams@gprojukti.com'


        except:
            pass
            
        return ResponseWrapper(data= serializer.data, msg='Succeed', status=200)    
   
    @log_activity
    def product_stock_transfer_received(self, request, requisition_no,  *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True, many = True)
        
        error_msg_list = []
        received_barcode_list = []
        not_received_barcode_list = []
        mismatch_barcode_list = []
        previous_received_barcode_list = []
         
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        qs = ProductStockTransfer.objects.filter(
            requisition_no = requisition_no
        ).last()
        
        if not qs:
            return ResponseWrapper(error_msg='Stock Transfer is not Found', error_code=404)
        
        received_barcode_all_list = request.data
        
        all_stock_transfer_barcode_list = qs.product_stock.values_list('barcode', flat = True)
        
        if qs.received_barcode_list:
            previous_received_barcode_list = eval(qs.received_barcode_list)
        
        for barcode in received_barcode_all_list:
            barcode_no = barcode.get('barcode')
            
            product_stock_qs = ProductStock.objects.filter(barcode= barcode_no).last()
            
            if not product_stock_qs:
                error_msg_list.append(f'This {barcode_no} Barcode is not Found')
            else:   
                received_barcode_qs = qs.product_stock.filter(barcode = barcode_no)
                
                if received_barcode_qs:
                    received_barcode_list.append(barcode_no)
                elif not received_barcode_qs:
                    mismatch_barcode_list.append(barcode_no)
                
        
        received_barcode_list.extend(previous_received_barcode_list)
        
        received_barcode_list = list(set(received_barcode_list))
        
        not_received_barcode_list = [barcode for barcode in all_stock_transfer_barcode_list if barcode not in received_barcode_list]
        
        qs.mismatch_barcode_list = str(mismatch_barcode_list)
        qs.not_received_barcode_list = str(not_received_barcode_list)
        qs.received_barcode_list = str(received_barcode_list)
        
        if mismatch_barcode_list or not_received_barcode_list:
            qs.status = "NOT_UPDATED"
        else:
            qs.status = "UPDATED"
            
        qs.save()
        
        status_change_reason = f"In #{requisition_no}, Those {qs.received_barcode_list} is Received and The Not Received Barcode is {qs.not_received_barcode_list} and also The Mismatch Barcode is {qs.mismatch_barcode_list}, The Current Requisition Status is {qs.get_status_display()}"
        
        product_stock_transfer_log(product_stock_transfer_qs= qs, request_user= request.user, status_change_reason=status_change_reason)
        
        # Save Logger for Tracking 
        try:
            activity_log(qs, request,serializer)
        except:
            pass
        
        serializer = ProductStockTransferSerializer(qs)
        if error_msg_list:
            return ResponseWrapper(data= serializer.data, msg=str(error_msg_list), status=200)
        
        return ResponseWrapper(data= serializer.data, msg='Succeed', status=200)
    
    
    @log_activity
    def update(self, request, requisition_no,  *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True) 
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        stock_transfer_qs = ProductStockTransfer.objects.filter(
            requisition_no = requisition_no
        ).last()
        
        if not stock_transfer_qs:
            return ResponseWrapper(error_msg='Stock Transfer is not Found', error_code=404)
        
        status_change_reason = serializer.validated_data.pop('status_change_reason')
        
        status = serializer.validated_data.get('status')
        
        if status in ['FAILED', 'ON_HOLD', 'CANCELLED'] and not status_change_reason:
            return ResponseWrapper(error_msg='Status Change Reason is Mandatory', error_code=4040)
        
        qs = serializer.update(instance=stock_transfer_qs, validated_data=serializer.validated_data)
        
        if qs.status == 'APPROVED':
            product_stock_qs = ProductStock.objects.filter(id__in = qs.product_stock.all())
            product_stock_qs.update(stock_location =qs.to_shop, status="ACTIVE")
            
        if qs:
            product_stock_transfer_log(product_stock_transfer_qs= qs, request_user= request.user, status_change_reason=status_change_reason)

        # Save Logger for Tracking 
        try:
            activity_log(qs, request,serializer)
        except:
            pass
        
        serializer = ProductStockTransferSerializer(instance=qs)
        
        return ResponseWrapper(data= serializer.data, msg='Succeed', status=200)
    
    @log_activity
    def retrieve(self, request, requisition_no,  *args, **kwargs):
        stock_transfer_qs = ProductStockTransfer.objects.filter(
            requisition_no = requisition_no
        ).last()
        
        if not stock_transfer_qs:
            return ResponseWrapper(error_msg='Stock Transfer is not Found', error_code=404)
        
        serializer = ProductStockTransferDetailsSerializer(stock_transfer_qs)
        return ResponseWrapper(data= serializer.data, msg='Succeed', status=200)
    
    @log_activity
    def stock_transfer_invoice_print(self, request, requisition_no, *args, **kwargs):
        qs = ProductStockTransfer.objects.filter(requisition_no=requisition_no).last()

        if not qs:
            return ResponseWrapper(error_msg='Product Stock Transfer is Not Found', status=404)

        product_codes = qs.product_stock.all()
        
        product_barcodes = {product_stock.barcode: product_stock.barcode.split('-')[0] for product_stock in product_codes}
        product_codes_set = set(product_barcodes.values())
        
        products = Product.objects.filter(product_code__in=product_codes_set)
        products_dict = {product.product_code: product.name for product in products}
        
        products_info = defaultdict(lambda: {'product_name': 'Unknown', 'barcodes': set(), 'barcode_count': 0})

        for barcode, product_code in product_barcodes.items():
            product_name = products_dict.get(product_code, 'Unknown')
            products_info[product_code]['product_name'] = product_name
            products_info[product_code]['barcodes'].add(barcode)
            products_info[product_code]['barcode_count'] += 1

        all_data_list = [{'product_name': info['product_name'],
                'product_code': product_code,
                'barcodes': ', '.join(info['barcodes']),
                'barcode_count': info['barcode_count']}
                for product_code, info in products_info.items()]

        context = {
            'product_name_list': [info['product_name'] for info in products_info.values()],
            'requisition_no': requisition_no,
            'from_shop_name': qs.from_shop.name,
            'to_shop_name': qs.to_shop.name,
            'data': all_data_list,
            'created_at': (qs.created_at + timedelta(hours=6)).strftime("%b %d, %Y at %I:%M %p"),
            'transfer_type': qs.get_stock_transfer_type_display(),
        }
        
        pdf= render_to_pdf('stock-transfer.html',context)
        if pdf:
            response=HttpResponse(pdf, content_type="application/pdf")
            
            # ....***.... Show PDF File ....***....
            content=f"inline; filename=Stock Transfer-{requisition_no}.pdf" 
            
            # # ....***.... Automated Download PDF File ....***....
            
            # content=f"attachment; filename=Stock Transfer-{requisition_no}.pdf"
            response['Content-Disposition']=content
            
        return response
        
      
class ProductStockRequisitionViewSet(CustomViewSet):
    queryset = ProductStockRequisition.objects.all()
    lookup_field = 'pk'
    serializer_class = ProductRequisitionListSerializer
    permission_classes = [CheckCustomPermission]
    
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.OrderingFilter,
    # )
    # filterset_class = ProductStockTransferFilter
    
    def get_filterset_class(self):
        if self.action in ['requisition_product_list']:
            self.filterset_class = ProductFilter
        else:
            self.filterset_class = None

        return self.filterset_class
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = ProductRequisitionCreateSerializer
        elif self.action in ['update']:
            self.serializer_class = ProductRequisitionUpdateSerializer
        elif self.action in ['product_stock_requisition_transfer']:
            self.serializer_class = ProductRequisitionTransferSerializer
        elif self.action in ['list']:
            self.serializer_class = ProductRequisitionListSerializer
        else:
            self.serializer_class = ProductRequisitionDetailsSerializer

        return self.serializer_class 

    @log_activity
    def create(self, request, *args,shop_slug, **kwargs):
        shop_qs = OfficeLocation.objects.filter(slug = shop_slug).last()
        if not shop_qs:
            return ResponseWrapper(error_msg='Shop is Not Found', error_code=404)
        
        employee_slug = request.data.get('employee_slug')
        item_list = request.data.get('item_list')
        
        employee_information_qs = EmployeeInformation.objects.filter(slug = employee_slug).last()
        if not employee_information_qs:
            return ResponseWrapper(error_msg='Employee is Not Found', error_code=404)
        
        last_stock_transfer_qs = ProductStockTransfer.objects.all().order_by('id').last()
        if last_stock_transfer_qs:
            last_requisition_no = last_stock_transfer_qs.requisition_no
        else:
            last_requisition_no = "REG00000001"
            
        requisition_no = generate_requisition_no(last_requisition_no)
        
        qs = ProductStockRequisition.objects.create(
            requisition_no = requisition_no,
            status = 'INITIALIZED',
            shop = shop_qs,
            approved_by = employee_information_qs,
            created_by = request.user
        )
        total_need_quantity = 0
        
        user_information_qs = UserInformation.objects.filter(
            user = request.user
        ).last()
        
        name = f"{request.user.first_name} {request.user.last_name}"
        
        if user_information_qs:
            name = user_information_qs.name
            
            status_changed_by = {
                'id': user_information_qs.id,
                'name': user_information_qs.name,
                'email': user_information_qs.user.email,
                'phone': user_information_qs.user.phone,
                'image': user_information_qs.image or '-',
            }
        
        order_status_reason = f"Requisition Created By {name} at {qs.created_at}"
        
        for item in item_list:
            product_slug = item.get('product_slug')
            needed_quantity = item.get('needed_quantity')
            
            if needed_quantity  < 1:
                return ResponseWrapper(error_msg='Quantity Must Be Gater Then 0', error_code=400)
            
            product_qs = Product.objects.filter(slug = product_slug).last()
            if not product_qs:
                return ResponseWrapper(error_msg='Product is Not Found', error_code=404)
            
            item_qs = ProductStockRequisitionItem.objects.create(
                needed_quantity = needed_quantity,
                status = 'INITIALIZED',
                product_stock_requisition = qs,
                product = product_qs,
                created_by = request.user   
            )
            
            item_log_qs = ProductStockRequisitionItemStatusLog.objects.create(
                product_stock_requisition_item_id = item_qs.id,
                status = status,
                status_display = 'Initialized',
                order_status_reason = order_status_reason,
                status_changed_by = status_changed_by,
                status_change_at = item_qs.created_at,
                created_by = request.user   
            )
            total_need_quantity +=needed_quantity
            
        qs.total_need_quantity = total_need_quantity
        qs.save()
        
        log_qs = ProductStockRequisitionStatusLog.objects.create(
            product_stock_requisition = qs,
            status = status,
            status_display = 'Initialized',
            order_status_reason = order_status_reason,
            status_changed_by = status_changed_by,
            status_change_at = qs.created_at,
            created_by = request.user   
        )

        try:
            subject = f"An Product Stock Requisition is Created"

            message_body = f"<html><p> Dear {request.user.first_name} {request.user.last_name}, </strong> <br> A Stock Requisition is Created By <strong>'{request.user.first_name} {request.user.last_name}' </strong>, And Requisition no is  = #{requisition_no} at {qs.created_at}.</p>Thank you, <br> G-Projukti.com </html>"

            send_email(email='setusakilanasrin@gmail.com',subject= subject, body=message_body)

        except:
            pass
        
        serializer = ProductRequisitionListSerializer(instance=qs)
        return ResponseWrapper(data = serializer.data, msg = 'Success', status=200)


    @log_activity
    def update(self, request, *args, requisition_no, **kwargs):
        requisition_qs = ProductStockRequisition.objects.filter(requisition_no = requisition_no).last()
        if not requisition_qs:
            return ResponseWrapper(error_msg='Requisition is Not Found', error_code=404)
        
        item_list = request.data.get('item_list')
        status = request.data.get('status')
        order_status_reason = request.data.get('order_status_reason')
        
        total_approved_quantity = 0
        
        requisition_qs.status = status
        requisition_qs.save()
        
        total_need_quantity = 0
        
        user_information_qs = UserInformation.objects.filter(
            user = request.user
        ).last()
        
        name = f"{request.user.first_name} {request.user.last_name}"
        
        if user_information_qs:
            name = user_information_qs.name
            
            status_changed_by = {
                'id': user_information_qs.id,
                'name': user_information_qs.name,
                'email': user_information_qs.user.email,
                'phone': user_information_qs.user.phone,
                'image': user_information_qs.image or '-',
            }
        
        if status in ['ON_HOLD', 'CANCELLED', 'FAILED'] and not order_status_reason:
            return ResponseWrapper(error_msg='Status Change Reason is Not Found', error_code=400)
            
        if not order_status_reason:
            order_status_reason = f"Requisition {status} By {name} at {requisition_qs.created_at}"
        
        for item in item_list:
            item_id = item.get('item_id')
            status = item.get('status')
            order_status_reason = item.get('order_status_reason')
            product_slug = item.get('product_slug')
            needed_quantity = item.get('needed_quantity')
            approved_quantity = item.get('approved_quantity')
            
            if status in ['ON_HOLD', 'CANCELLED', 'FAILED'] and not order_status_reason:
                return ResponseWrapper(error_msg='Status Change Reason is Not Found', error_code=400)
            
            if needed_quantity and needed_quantity  < 1:
                return ResponseWrapper(error_msg='Quantity Must Be Gater Then 0', error_code=400)
            
            if product_slug:
                product_qs = Product.objects.filter(slug = product_slug).last()
                if not product_qs:
                    return ResponseWrapper(error_msg='Product is Not Found', error_code=404)
            
            if item_id:
                requisition_item_qs = ProductStockRequisitionItem.objects.filter(id = item_id).last()
                if not requisition_item_qs:
                    return ResponseWrapper(error_msg='Requisition Item Is Not Found', error_code=400)
                
                status = status if status else requisition_item_qs.status
                needed_quantity = needed_quantity if needed_quantity else requisition_item_qs.needed_quantity
                
                product_qs = requisition_item_qs.product
                
                requisition_item_qs.status = status
                requisition_item_qs.approved_quantity = approved_quantity
                requisition_item_qs.status_changed_by = status_changed_by
                requisition_item_qs.save()
                
                total_approved_quantity += approved_quantity
                total_need_quantity += needed_quantity
                
            
            else:
                requisition_item_qs = ProductStockRequisitionItem.objects.create(
                    needed_quantity = needed_quantity,
                    status = status,
                    product_stock_requisition = requisition_qs,
                    product = product_qs,
                    created_by = request.user   
                )
                total_need_quantity += needed_quantity
                
            status_display = requisition_item_qs.get_status_display()
                
            item_log_qs = ProductStockRequisitionItemStatusLog.objects.create(
                product_stock_requisition_item_id = requisition_item_qs.id,
                status = status,
                status_display = status_display,
                order_status_reason = order_status_reason,
                status_changed_by = status_changed_by,
                status_change_at = requisition_item_qs.created_at,
                created_by = request.user   
            )
            
        requisition_qs.total_need_quantity = total_need_quantity
        requisition_qs.total_approved_quantity = total_approved_quantity
        
        if status == 'APPROVED':
            employee_qs = EmployeeInformation.objects.filter(user = request.user).last()
            if not employee_qs:
                return ResponseWrapper(error_msg='{request.user} Have Not Enough Permission', error_code=400)
            
            requisition_qs.approved_by = employee_qs
            
        if status == 'DELIVERED':
            product_stock_transfer_qs = ProductStockTransfer.objects.filter(product_requisition__requisition_no = requisition_no).last()
            
            if product_stock_transfer_qs:
                product_stock_qs = ProductStock.objects.filter(id__in = product_stock_transfer_qs.product_stock.all())
                product_stock_qs.update(stock_location =product_stock_transfer_qs.to_shop)
                
        requisition_qs.save()
        
        status_display = requisition_qs.get_status_display()
        
        log_qs = ProductStockRequisitionStatusLog.objects.create(
            product_stock_requisition = requisition_qs,
            status = status,
            status_display = status_display,
            order_status_reason = order_status_reason,
            status_changed_by = status_changed_by,
            status_change_at = requisition_qs.created_at,
            created_by = request.user   
        )
            
        serializer = ProductRequisitionDetailsSerializer(instance=requisition_qs)
        return ResponseWrapper(data = serializer.data, msg = 'Success', status=200)
        

    @log_activity
    def product_stock_requisition_transfer(self, request, *args, requisition_no, **kwargs):
        requisition_qs = ProductStockRequisition.objects.filter(requisition_no = requisition_no).last()
        if not requisition_qs:
            return ResponseWrapper(error_msg='Requisition is Not Found', error_code=404)
        
        if requisition_qs.status != 'PURCHASED':
            return ResponseWrapper(error_msg='Requisition is Not Ready for Transfer', error_code=400)
        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        from_shop = request.data.get('from_shop')
        from_shop_qs = OfficeLocation.objects.filter(slug = from_shop).last()
        to_shop_qs = OfficeLocation.objects.filter(slug = requisition_qs.shop.slug).last()
        
        if not from_shop_qs:
            return  ResponseWrapper(error_msg='From Shop is Not Found', error_code=404)
        
        if from_shop_qs == to_shop_qs:
            return  ResponseWrapper(error_msg='From Shop and Destination Shop is Same', error_code=400)
        
        approved_by_qs = EmployeeInformation.objects.filter(user__id = request.user.id).last()
        
        product_stock_list = request.data.get('product_stock')
        if not product_stock_list:
            return ResponseWrapper(error_msg=f'Barcode is Mandatory', error_code=404)
        
        
        product_stock_qs = ProductStock.objects.filter(barcode__in=product_stock_list, status='ACTIVE').values_list('barcode', flat=True)
        
        product_stock_qs_list = list(product_stock_qs)  # Convert queryset to a list

        # Find missing barcodes
        missing_barcodes = set(product_stock_list) - set(product_stock_qs_list)

        if missing_barcodes:
            return ResponseWrapper(msg=f'These barcodes are not found: {missing_barcodes}', status=400)
        
        product_stock = set(serializer.validated_data.pop('product_stock', None)) 
        
        product_stock_transfer_qs = ProductStockTransfer.objects.filter(product_stock__barcode__in = product_stock_list, status__in = ['IN_TRANSIT', 'UPDATED']).last()
        
        if product_stock_transfer_qs:
            product_stock_transfer_log(product_stock_transfer_qs= product_stock_transfer_qs, request_user= request.user, status_change_reason=None)
             
            return ResponseWrapper(error_msg=f'Products is Already In a Requisition, which is # {product_stock_transfer_qs.requisition_no} and the status is {product_stock_transfer_qs.get_status_display()}', error_code=400)
        
        product_barcode = [item.split('-')[0] for item in product_stock]
        barcode_counts = Counter(product_barcode)
        
        product_codes = set(barcode_counts.keys())
        
        product_stocks = ProductStock.objects.filter(barcode__in=product_codes).select_related('product_price_info__product')
        
        product_map = {product_stock.barcode: product_stock.product for product_stock in product_stocks}
        
        for barcode, count in barcode_counts.items():
            # if barcode not in product_map:
            #     return ResponseWrapper(error_msg=f"{barcode} is Not Found", error_code=404)
            
            product_qs = Product.objects.filter(product_code = barcode).last()
            
            requisition_item_qs = ProductStockRequisitionItem.objects.filter(product_stock_requisition = requisition_qs, product=product_qs).last()
             
            if requisition_item_qs is None:
                return ResponseWrapper(error_msg=f"For '{product_qs.name}', no requisition item found", error_code=404)
            
            if requisition_item_qs.approved_quantity != count:
                return ResponseWrapper(error_msg=f"For '{product_qs.name}'({barcode}) Need '{requisition_item_qs.approved_quantity}' Product", error_code=400) 
        
        qs = serializer.save(
                requisition_no=requisition_no,
                created_by=request.user,
                from_shop=from_shop_qs,
                to_shop=to_shop_qs,
                approved_by = approved_by_qs,
                product_requisition = requisition_qs,
                status = 'IN_TRANSIT',
                stock_transfer_type = 'REQUISITION'
            )
        
        requisition_qs.status = 'IN_TRANSIT'
        requisition_qs.save()
        
        
        for barcode in product_stock_list:
            product_stock_qs = ProductStock.objects.filter(barcode = barcode).last()
            if product_stock_qs:
                if qs.stock_transfer_type == 'REQUISITION':
                    product_stock_qs.status = 'IN_REQUISITION'
                    
                    qs.product_stock.add(product_stock_qs)
                    product_stock_qs.save()
            else:
                return ResponseWrapper(msg=f'This {barcode}, is Not Found', status=400)
            
        serializer = ProductStockTransferDetailsSerializer(instance=qs)
        
        status_change_reason =f"The Requisition ID is = #{requisition_no}, Status is {qs.get_status_display()},and also Shop is {qs.shop.name},  and Total Need Quantity is = {qs.total_need_quantity}, and Total Approved Quantity id  {qs.total_approved_quantity}"
        
        if qs:
            product_stock_transfer_log(product_stock_transfer_qs= qs, request_user= request.user, status_change_reason=status_change_reason)
             
        return ResponseWrapper(data= serializer.data, msg='Succeed', status=200)  
    
    @log_activity
    def retrieve(self, request,requisition_no,  *args, **kwargs):
        requisition_qs = ProductStockRequisition.objects.filter(requisition_no = requisition_no).last()
        if not requisition_qs:
            return ResponseWrapper(error_msg='Requisition is Not Found', error_code=404)
        serializer = ProductRequisitionDetailsSerializer(instance=requisition_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    
    @log_activity
    def requisition_shop_list(self, request, *args, **kwargs):
        store_qs = get_user_store_list(request.user)
        qs = store_qs.filter(office_type__in = ['STORE'])
        
        product_qs = Product.objects.filter(product_price_infos__product_stocks__stock_location__slug__in = qs.values_list('slug', flat=True))
        
        serializer = ProductRequisitionShopListSerializer(instance=qs, many = True)
        return ResponseWrapper(data = serializer.data, msg = 'Success', status=200)
    
    @log_activity
    def requisition_product_list(self, request, shop_slug, *args, **kwargs):
        product_slugs = ProductStock.objects.filter(stock_location__slug=shop_slug).values_list('product_price_info__product__slug', flat=True).distinct()
        
        search = request.GET.get('search')
        
        product_qs = Product.objects.filter(slug__in=product_slugs).exclude(status = "CHILD").order_by('-id')
        
        if search:
            product_qs = product_qs.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(product_code__icontains = search)
            ).distinct()
        
        
        page_qs = self.paginate_queryset(product_qs)
        
        serializer = ProductRequisitionProductListSerializer(instance=page_qs, many = True)
        
        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data = paginated_data.data, msg = 'Success', status=200)


class ProductStockTransferDownloadViewSet(CustomViewSet):
    queryset = ProductStockTransfer.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = ProductStockSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductStockTransferFilter
    
    def get_permissions(self):
        if self.action in ["product_stock_list"]:
            permission_classes = [
                    (CheckCustomPermission("can_view_list_product_stock"))
                ]
        if self.action in ["list"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @staticmethod
    async def generate_excel(serializer_data):
        df = pd.DataFrame(serializer_data)
        stream = io.BytesIO()
        df.to_excel(stream, index=False)
        stream.seek(0)
        return stream.getvalue()

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    @log_activity
    def list(self, request, *args, **kwargs):
        import pytz
        from datetime import datetime
        from django.db import connection
        import pandas as pd

        # Get search parameters
        requisition_no = request.GET.get('search')
        from_shop = request.GET.get('from_shop')
        to_shop = request.GET.get('to_shop')
        status = request.GET.get('status')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        stock_transfer_type = request.GET.get('stock_transfer_type')

        # Base SQL query
        query = """
        SELECT 
            pst.id AS "SI",
            pst.requisition_no AS "Requisition No",
            INITCAP(REPLACE(LOWER(pst.status), '_', ' ')) AS "Status",
            INITCAP(REPLACE(LOWER(pst.stock_transfer_type), '_', ' ')) AS "Stock Transfer Type",
            from_shop.name AS "From Shop",
            to_shop.name AS "To Shop",
            array_agg(ps.barcode) AS "Transfer Stock List",
            pst.mismatch_barcode_list AS "Mismatch Barcode List",
            pst.not_received_barcode_list AS "Not Received Barcode List",
            pst.received_barcode_list AS "Received Barcode List",
            ei.name AS "Approved By",
            log.created_at AS "Status Update Date"
        FROM 
            product_management_productstocktransfer pst
        LEFT JOIN 
            location_officelocation from_shop ON pst.from_shop_id = from_shop.id
        LEFT JOIN 
            location_officelocation to_shop ON pst.to_shop_id = to_shop.id
        LEFT JOIN 
            human_resource_management_employeeinformation ei ON pst.approved_by_id = ei.id
        LEFT JOIN 
            product_management_productstocktransfer_product_stock ps_transfer ON pst.id = ps_transfer.productstocktransfer_id
        LEFT JOIN 
            product_management_productstock ps ON ps_transfer.productstock_id = ps.id
        LEFT JOIN 
            product_management_productstocktransferlog log ON pst.id = log.product_stock_id
        WHERE 
            pst.is_active = TRUE
        """

        # Append conditions based on search parameters
        params = []
        if start_date_str and end_date_str:
            # take month-date-year
            query += " AND log.created_at BETWEEN %s AND %s"
            params.append(start_date_str)
            params.append(end_date_str)
        if requisition_no:
            query += " AND pst.requisition_no = %s"
            params.append(requisition_no)
        if from_shop:
            query += " AND from_shop.name = %s"
            params.append(from_shop)
        if to_shop:
            query += " AND to_shop.name = %s"
            params.append(to_shop)
        if status:
            query += " AND pst.status = %s"
            params.append(status)
        if stock_transfer_type:
            query += " AND pst.stock_transfer_type = %s"
            params.append(stock_transfer_type)

        query += " GROUP BY pst.id, from_shop.name, to_shop.name, ei.name, log.created_at"

        # Execute the query and fetch results
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Convert timezone-aware datetimes to naive datetimes
        for col in df.select_dtypes(include=['datetime64[ns, UTC]']).columns:
            df[col] = df[col].dt.tz_localize(None)

        # Generate Excel file asynchronously
        excel_content = async_to_sync(self.generate_excel)(df)

        # Create the HttpResponse object with the appropriate XLSX content-type and headers
        response = HttpResponse(excel_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Get today's date in the format you want
        today_date = datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d')

        # Construct the filename with today's date
        filename = f'Product Stock Transfer - {today_date}.xlsx'

        # Assign the filename to the Content-Disposition header
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class ProductStockLogDownloadViewSet(CustomViewSet):
    queryset = ProductStockLog.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = ProductStockLogSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductStockLogFilter

    def get_permissions(self):
        # if self.action in ["product_stock_list"]:
        #     permission_classes = [
        #             (CheckCustomPermission("can_view_list_product_stock"))
        #         ]
        # else:The SQL code you've provided seems generally correct in terms of syntax and structure. However, there are a few things to consider or potentially improve upon:


        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @log_activity
    def list(self, request, *args, **kwargs):
        from django.db import connection
        import pytz
        from datetime import datetime

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        stock_location = request.GET.get('stock_location')
        status = request.GET.get('status')
        search = request.GET.get('search')

        # Construct SQL query with dynamic filtering
        query = """
            SELECT
                ROW_NUMBER() OVER () AS "SI",
                DATE(psl.created_at AT TIME ZONE 'UTC') AS "Order Date",
                ps.barcode AS "Product Barcode",
                COALESCE(prp.name, '-') AS "Parent Product Name",  -- Handle null parent gracefully
                COALESCE(prp.product_code, '-') AS "Parent Product Code",  -- Handle null parent gracefully
                INITCAP(REPLACE(LOWER(ps.status), '_', ' ')) AS "Product Status",
                DATE(ps.stock_in_date AT TIME ZONE 'UTC') AS "Stock In Date",
                psl.stock_in_age AS "Stock In Age",
                psl.stock_location_info ->> 'name' AS Name,
                psl.current_status_display AS "Current Stock Status Display",
                psl.previous_status_display AS "Previous Stock Status Display",
                psl.remarks AS "Remarks",
                psl.stock_status_change_by_info -> 'user_details' ->> 'name' AS "Stock Status Change User Name",
                psl.stock_status_change_by_info ->> 'phone' AS "Stock Status Change User Phone",
                psl.stock_status_change_by_info ->> 'email' AS "Stock Status Change User Email"
            FROM
                product_management_productstocklog psl
            LEFT JOIN
                product_management_productstock ps ON psl.product_stock_id = ps.id
            LEFT JOIN
                product_management_productpriceinfo psi ON ps.product_price_info_id = psi.id
            LEFT JOIN
                product_management_product prd ON psi.product_id = prd.id
            LEFT JOIN
                product_management_product prp ON prd.product_parent_id = prp.id
            WHERE 1=1
        """

        params = {}

        # Check if the date range is greater than 31 days
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%m-%d-%Y')
            end_date = datetime.strptime(end_date, '%m-%d-%Y')
            date_diff = (end_date - start_date).days

            if date_diff > 31:
                return ResponseWrapper(error_msg='Date range should not be more than 31 days', error_code=400)
            else:
                query += " AND DATE(ps.stock_in_date AT TIME ZONE 'UTC') BETWEEN %(start_date)s AND %(end_date)s"
                params['start_date'] = start_date.strftime('%Y-%m-%d')
                params['end_date'] = end_date.strftime('%Y-%m-%d')

        if search:
            query += """
                AND (
                    ps.barcode ILIKE %(search)s OR
                    psl.current_status ILIKE %(search)s OR
                    psl.previous_status ILIKE %(search)s
                )
            """
            params['search'] = f'%{search}%'

        # Add stock_location filter if specified
        if stock_location:
            query += " AND psl.stock_location_info ->> 'name' = %(stock_location)s"
            params['stock_location'] = stock_location

        if status:
            query += """
                AND INITCAP(REPLACE(LOWER(ps.status), '_', ' ')) = %(status)s
            """
            # Adjust status to match the format of the database field
            formatted_status = status.replace('_', ' ').lower().capitalize()
            params['status'] = formatted_status

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        # Check if there is any data to serialize
        if not rows:
            return ResponseWrapper(error_msg='No data found', error_code=400)

        # Define the headers
        headers = [
            'SI', 'Order Date', 'Product Barcode',  'Parent Product Name', 'Parent Product Code', 'Product Status', 'Stock In Date', 'Stock In Age', 'Stock Location Info',
            'Current Stock Status Display', 'Previous Stock Status Display',
            'Remarks',  'Stock Status Change User Name', 'Stock Status Change User Phone', 'Stock Status Change User Email',
        ]

        # Create an XLSX file
        wb = Workbook()
        ws = wb.active

        # Write headers to the first row
        ws.append(headers)

        # Write data rows
        for row in rows:
            # Convert timezone-aware datetimes to naive datetimes
            row_data = []
            for value in row:
                if isinstance(value, datetime):
                    # Convert timezone-aware datetime to naive datetime
                    if value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                row_data.append(value)
            ws.append(row_data)

        # Get today's date
        today_date = datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d')

        # Create a file-like response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=product_stock_logs_{today_date}.xlsx'

        # Save workbook to response
        wb.save(response)

        return response


class ShopWiseZeroStockLogViewSet(CustomViewSet):
    queryset = ShopWiseZeroStockLog.objects.all().order_by("?")
    lookup_field = 'pk'
    serializer_class = ShopWiseZeroStockLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ShopWiseZeroStockLogFilter


from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

import logging

# Configure logging
logger = logging.getLogger(__name__)


# class ShopWiseBarcode(APIView):
#     """
#     Retrieve all barcodes and corresponding product slugs for a specific shop (store) based on store_slug.
#     """

#     def get(self, request, *args, **kwargs):
#         store_slug = kwargs.get('store_slug')

#         # Retrieve the OfficeLocation using slug
#         store = get_object_or_404(OfficeLocation, slug=store_slug, is_active=True)

#         # Query all active ProductStock instances for the store with related ProductPriceInfo and Product
#         product_stocks = ProductStock.objects.filter(
#             stock_location=store,
#             status='ACTIVE',
#             is_active=True
#         ).select_related('product_price_info__product')  # Optimize queries

#         # Serialize the data
#         serializer = ProductStockSerializer2(product_stocks, many=True)

#         # Extract serialized data
#         serialized_data = serializer.data

#         if not serialized_data:
#             return Response({
#                 'data': [],
#                 'msg': 'No barcodes found for the specified store.',
#                 'status': 200
#             }, status=status.HTTP_200_OK)

#         return Response({
#             'data': serialized_data,
#             'msg': 'Success',
#             'status': 200
#         }, status=status.HTTP_200_OK)


import requests
class ShopWiseBarcode(APIView):
    """
    Retrieve all barcodes and corresponding product slugs for a specific shop (store) based on store_slug.
    Additionally, create an order for each barcode by calling an external API.
    """

    # External API configuration
    EXTERNAL_API_URL = "https://productionapi.gprojukti.com/v2.0/order/admin/order/"
    AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NDU0NjE4LCJpYXQiOjE3MjgxOTU0MTgsImp0aSI6IjM2Nzk4Y2VmNmExMjRkZWY4ZGRlMzJkYmUwZmMwY2Y5IiwidXNlcl9pZCI6NDI1Njh9.RAuclrYqSQFIefbTi4kh4e31i0PFWdHpjB3J_U1C9KM"

    def get(self, request, *args, **kwargs):
        store_slug = kwargs.get('store_slug')

        # Retrieve the OfficeLocation using slug
        store = get_object_or_404(OfficeLocation, slug=store_slug, is_active=True)

        # Query all active ProductStock instances for the store with related ProductPriceInfo and Product
        product_stocks = ProductStock.objects.filter(
            stock_location=store,
            status='ACTIVE',
            is_active=True
        ).select_related('product_price_info__product')  # Optimize queries
       
        # Serialize the data
        serializer = ProductStockSerializer2(product_stocks, many=True)

        # Extract serialized data
        serialized_data = serializer.data

        if not serialized_data:
            return Response({
                'data': [],
                'msg': 'No barcodes found for the specified store.',
                'status': 200
            }, status=status.HTTP_200_OK)

        # Iterate over each serialized barcode and create an order
        for item in serialized_data:
            payload = {
                "first_name": "shop closing sale",
                "last_name": "",
                "email": "",
                "phone": "01666666666",
                "area_slug": "dhaka-cantonment-5bky-07-7456-160132-09-7456-2024",
                "address": "Dhaka",
                "address_type": "HOME",
                "remarks": "shop closing sale",
                "delivery_method_slug": "store-sell",
                "order_type": "POINT_OF_SELL",
                "payment_type": "",
                "promo_code": "",
                "is_for_employee": False,
                "created_by": "",
                "order_item_list": [
                    {
                        "quantity": 1,
                        "product_slug": item.get('product_slug'),
                        "selling_price": item.get('msp'),
                        "gsheba_amount": 0,
                        "created_by": "1469",
                        "barcode_number": item.get('barcode')
                    }
                ],
                "order_payment_list": [
                    {
                        "transaction_no": "",
                        "payment_method_slug": "cod",
                        "received_amount": item.get('msp')
                    }
                ]
            }

            headers = {
                "Authorization": self.AUTH_TOKEN,
                "Content-Type": "application/json"
            }

            try:
                response = requests.post(self.EXTERNAL_API_URL, json=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                logger.info(f"Order created successfully for barcode: {item.get('barcode')}")
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP error occurred for barcode {item.get('barcode')}: {http_err}")
            except Exception as err:
                logger.error(f"An error occurred for barcode {item.get('barcode')}: {err}")

        return Response({
            'data': serialized_data,
            'msg': 'Success and orders created.',
            'status': 200
        }, status=status.HTTP_200_OK)