from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from human_resource_management.models.employee import EmployeeInformation
from product_management.filter.brand_seller import *
from utils.actions import activity_log
from utils.generates import unique_slug_generator
from utils.response_wrapper import ResponseWrapper

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from utils.decorators import log_activity

# User = get_user_model()
from rest_framework.permissions import IsAdminUser
from utils.permissions import CheckCustomPermission
# import re
from product_management.models.brand_seller import *
from product_management.serializers.brand_seller import *

from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet, object_get
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from utils.upload_image import image_upload


class BrandViewSet(CustomViewSet):
    queryset = Brand.objects.all()
    lookup_field = 'pk'
    serializer_class = BrandSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = BrandFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = BrandSerializer
        elif self.action in ['list']:
            self.serializer_class = BrandListSerializer
        else:
            self.serializer_class = BrandDetailsSerializer

        return self.serializer_class
    
        # ..........***.......... Create ..........***..........
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        if serializer.is_valid():
            image_file = request.data.get('logo')
            image_file  = serializer.validated_data.pop('logo', None)
            # image_file = None
            
            path = 'brand'
            
            name = serializer.validated_data.get('name', '')
            
            qs = self.queryset.filter(name=name)
            
            if qs.exists():
                return ResponseWrapper(error_msg="Brand is Already Found", error_code=400)
            
            slug = unique_slug_generator(name=name) if name else None
            if image_file:
                logo = image_upload(file=image_file, path=path)
            else:
                logo = None
            
            instance = serializer.save(
                created_by=request.user,
                logo=logo,
                slug=slug,
            )
            
            serializer = BrandDetailsSerializer(instance=instance)
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            last_error_msg = serializer.errors.popitem()
            last_error_full_msg = f"For '{last_error_msg[0]}', Need {str(last_error_msg[1][0])}"

            return ResponseWrapper(error_msg=last_error_full_msg, error_code=400)


    
        # ..........***.......... Create ..........***..........
    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            last_error_msg = serializer.errors.popitem()
            last_error_full_msg = f"For '{last_error_msg[0]}', Need {str(last_error_msg[1][0])}"

            return ResponseWrapper(error_msg=last_error_full_msg, error_code=400)
        
        qs =  self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_msg='Brand Is Not Found', error_code=404)

        image_file = request.data.get('logo')
        image_file  = serializer.validated_data.pop('logo', None)
        
        path = 'brand'
        
        name = serializer.validated_data.get('name', '')
        
        brand_qs = self.queryset.exclude(slug = qs.slug).filter(name=name)
     
        if brand_qs.exists():
            return ResponseWrapper(error_msg="Brand is Already Found", error_code=400)
        
        slug = unique_slug_generator(name=name) if name else None

        if image_file:
            logo_url = image_upload(file=image_file, path=path)
        else:
            logo_url = None
        
        instance = serializer.update(
            instance=qs, 
            validated_data=serializer.validated_data,
            )
        
        instance.logo = logo_url
        instance.updated_by_id = request.user.id
        instance.save()
        
        serializer = BrandDetailsSerializer(instance=instance)
        
        return ResponseWrapper(data=serializer.data, msg='created', status=200)
       

class SupplierViewSet(CustomViewSet):
    queryset = Supplier.objects.all()
    lookup_field = 'pk'
    serializer_class = SupplierSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SupplierFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = SupplierCreateUpdateSerializer
        else:
            self.serializer_class = SupplierSerializer

        return self.serializer_class
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        brand_slug  = request.data.pop('brand', None)
        
        if serializer.is_valid():
            image_file = request.data.get('logo')
            image_file  = serializer.validated_data.pop('logo', None)
            
            # brand_slug  = serializer.validated_data.pop('brand', None)
            # image_file = None
            
            path = 'supplier'
            
            name = serializer.validated_data.get('name', '')
            
            qs = self.queryset.filter(name=name)
            
            if qs.exists():
                return ResponseWrapper(error_msg="Supplier is Already Found", error_code=400)
            
            slug = unique_slug_generator(name=name) if name else None
            
            if image_file:
                logo = image_upload(file=image_file, path=path)
            else:
                logo = None
            
            # if not brand_slug:
            #     return ResponseWrapper(error_msg='Brand Name is Mandatory', error_code=400)
            
            instance = serializer.save(
                created_by=request.user,
                logo=logo,
                slug=slug,
            )
            # brand_qs = Brand.objects.filter(
            #     slug = brand_slug
            # ).last()
            # if not brand_qs:
            #     return ResponseWrapper(error_msg='Brand is Not Found', error_code=400)
            
            # instance.brand =  brand_qs
            # instance.save()
            
            
            serializer = SupplierSerializer(instance=instance)
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            last_error_msg = serializer.errors.popitem()
            last_error_full_msg = f"For '{last_error_msg[0]}', Need {str(last_error_msg[1][0])}"

            return ResponseWrapper(error_msg=last_error_full_msg, error_code=400)
        
        # ..........***.......... Create ..........***..........
    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if not serializer.is_valid():
            last_error_msg = serializer.errors.popitem()
            last_error_full_msg = f"For '{last_error_msg[0]}', Need {str(last_error_msg[1][0])}"

            return ResponseWrapper(error_msg=last_error_full_msg, error_code=400)
        
        qs =  self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_msg='Supplier Is Not Found', error_code=404)

        image_file = request.data.get('logo')
        image_file  = serializer.validated_data.pop('logo', None)
        brand_slug  = serializer.validated_data.pop('brand', None)
        
        path = 'supplier'
        
        name = serializer.validated_data.get('name', '')
        
        supplier_qs = self.queryset.exclude(slug = qs.slug).filter(slug=slug)
        
        if supplier_qs.exists():
            return ResponseWrapper(error_msg="Supplier is Already Found", 
                                   error_code=400)
        
        slug = unique_slug_generator(name=name) if name else None

        if image_file:
            logo = image_upload(file=image_file, path=path)
        else:
            logo = None
        
        
        serializer.update(instance=qs,
                          validated_data=serializer.validated_data)
        try:
            brand_qs = Brand.objects.filter(
                slug = brand_slug
            ).last()
            if not brand_qs:
                return ResponseWrapper(error_msg='Brand is Not Found', error_code=400)
            
            if qs:
                qs.updated_by_id = self.request.user.id
                qs.brand =  brand_qs
                
                qs.save()
        except:
            qs = qs
            
        serializer = BrandSerializer(instance=qs)
        
        return ResponseWrapper(data=serializer.data, msg='created', status=200)
       


class SellerViewSet(CustomViewSet):
    queryset = Seller.objects.all()
    lookup_field = 'pk'
    serializer_class = SellerSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SellerFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = SellerCreateUpdateSerializer
        else:
            self.serializer_class = SellerSerializer

        return self.serializer_class

    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        brand_slug  = request.data.pop('brand', None)
        
        if serializer.is_valid():
            image_file = request.data.get('logo')
            image_file  = serializer.validated_data.pop('logo', None)
            
            # image_file = None
            
            path = 'seller'
            
            name = serializer.validated_data.get('name', '')
            
            qs = self.queryset.filter(name=name)
            
            if qs.exists():
                return ResponseWrapper(error_msg="Seller is Already Found", error_code=400)
            
            slug = unique_slug_generator(name=name) if name else None
            
            if image_file:
                logo = image_upload(file=image_file, path=path)
            else:
                logo = None
            
            # if not brand_slug:
            #     return ResponseWrapper(error_msg='Brand Name is Mandatory', error_code=400)
            
            instance = serializer.save(
                created_by=request.user,
                logo=logo,
                slug=slug,
            )
            # brand_qs = Brand.objects.filter(
            #     slug = brand_slug
            # ).last()
            # if not brand_qs:
            #     return ResponseWrapper(error_msg='Brand is Not Found', error_code=400)
            
            # instance.brand =  brand_qs
            # instance.save()
            
            
            serializer = SellerSerializer(instance=instance)
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            last_error_msg = serializer.errors.popitem()
            last_error_full_msg = f"For '{last_error_msg[0]}', Need {str(last_error_msg[1][0])}"

            return ResponseWrapper(error_msg=last_error_full_msg, error_code=400)
        
        # ..........***.......... Create ..........***..........
    @log_activity
    def update(self, request, slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        code  = request.data.pop('code', None)
        
        if not serializer.is_valid():
            last_error_msg = serializer.errors.popitem()
            last_error_full_msg = f"For '{last_error_msg[0]}', Need {str(last_error_msg[1][0])}"

            return ResponseWrapper(error_msg=last_error_full_msg, error_code=400)
        
        qs =  self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_msg='Seller Is Not Found', error_code=404)

        
        image_file = request.data.get('logo')
        image_file  = serializer.validated_data.pop('logo', None)
        brand_slug  = serializer.validated_data.pop('brand', None)
        
        path = 'seller'
        
        name = serializer.validated_data.get('name', '')
        
        seller_qs = self.queryset.exclude(slug = qs.slug).filter(slug=slug)
        
        if seller_qs.exists():
            return ResponseWrapper(error_msg="Seller is Already Found", error_code=400)
        
        slug = unique_slug_generator(name=name) if name else None
        

        if image_file:
            logo = image_upload(file=image_file, path=path)
        else:
            logo = None
        
        
        serializer.update(instance=qs,
                          validated_data=serializer.validated_data)
        try:
            brand_qs = Brand.objects.filter(
                slug = brand_slug
            ).last()
            
            if not brand_qs:
                return ResponseWrapper(error_msg='Brand is Not Found', error_code=400)
            
            if qs:
                qs.logo = logo
                qs.updated_by_id = self.request.user.id
                qs.brand_id =  brand_qs.id
                
                qs.save()
        except:
            qs = qs
            
        serializer = SellerSerializer(instance=qs)
        
        return ResponseWrapper(data=serializer.data, msg='Successfully Updated', status=200)
       
