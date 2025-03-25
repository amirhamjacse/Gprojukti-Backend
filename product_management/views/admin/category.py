from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from human_resource_management.models.employee import EmployeeInformation
from product_management.filter.category import *
from utils.actions import activity_log
from utils.generates import *
from utils.response_wrapper import ResponseWrapper

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


# User = get_user_model()
from rest_framework.permissions import IsAdminUser
from utils.permissions import CheckCustomPermission
# import re
from product_management.models.category import *
from product_management.serializers.category import *

from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet, object_get
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from utils.decorators import log_activity

from utils.upload_image import image_upload


class CategoryGroupViewSet(CustomViewSet):
    queryset = CategoryGroup.objects.all()
    lookup_field = 'pk'
    serializer_class = CategoryGroupSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CategoryGroupFilter
    
    
    # ..........***.......... Create ..........***..........
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        image = request.data.get('image')
        
        if request.data.get('image') or image == []:
            image_file = None
            
        request.data.pop('image', None)
        
        if serializer.is_valid():
            image_file = serializer.validated_data.pop('image', None)
            
            path = 'category-group'
            
            name = serializer.validated_data.get('name', '')
            
            qs = self.queryset.filter(name=name)
            
            if qs.exists():
                return ResponseWrapper(error_msg="Category Group Name is Already Found", error_code=400)
            
            slug = unique_slug_generator_for_product_category(name=name) if name else None
            
            employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            if not employee_qs or not employee_qs.employee_company:
                return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
            company_id = employee_qs.employee_company

            if image_file: 
                banner_image = image_upload(file=image_file, path=path)
            else:
                banner_image = None
            
            instance = serializer.save(
                created_by=request.user,
                banner_image=banner_image,
                slug=slug,
                company=company_id
            )
            
            # activity_log(instance, request, serializer)
            
            serializer = CategoryGroupSerializer(instance=instance)
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


    # ..........***.......... Update ..........***..........
    @log_activity
    def update(self, request, **kwargs):
        slug = None
        if request.data.get("slug"):
            slug = request.data.pop("slug")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        image = request.data.get('image')
        
        if request.data.get('image') or image == []:
            image_file = None
            
        # request.data.pop('image', None)
        
        if serializer.is_valid():
            image_file = serializer.validated_data.pop('image', None)
            object_qs = self.queryset
            qs = object_get(object_qs, **kwargs)

            if not qs:
                return ResponseWrapper(error_code=406, error_msg='Not Found', 
                status=406)
            
            # ....NOTE...: Unique Slug Check :....START....

            if slug and kwargs.get("slug"):
                slug_check_qs = self.queryset.filter(slug = slug).exclude(slug = kwargs.get("slug"))
                if slug_check_qs:
                    return ResponseWrapper(error_code=406, error_msg='Slug is Already Exist', status=406)
                
            else:
                pk_check_qs = self.queryset.filter(pk = kwargs.get("pk")).exclude(pk = kwargs.get("pk"))
                if pk_check_qs:
                    return ResponseWrapper(error_code=406, error_msg='Slug is Already Exist', status=406)
            
            # ....NOTE...: Unique Slug Check :....END....
            
            if image_file:
                path = 'category-group'
                banner_image = image_upload(file=image_file, path=path)
                
                if banner_image:
                    qs = serializer.update(
                        instance=qs,
                        validated_data=serializer.validated_data
                        )
                    qs.banner_image = banner_image
                    qs.save()
            else:
                qs = serializer.update(instance=qs, validated_data=serializer.validated_data)
                

            if slug:
                qs.slug = slug
                qs.save()

            try:
                if qs:
                    qs.updated_by_id = self.request.user.id
                    qs.save()
            except:
                qs = qs

            serializer = CategoryGroupSerializer(instance=qs)

            # Save Logger for Tracking 
            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='Successfully Update')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    lookup_field = 'pk'
    serializer_class = CategorySerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CategoryFilter
    
    def get_serializer_class(self):
        if self.action in ['list']:
            self.serializer_class = CategoryListSerializer
        else:
            self.serializer_class = CategorySerializer

        return self.serializer_class
    
    # ..........***.......... Create ..........***..........
    @log_activity
    def category_overview_list(self, request, *args, **kwargs):
        context = [
            {
                'msg': "Total Category",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Sub-Category",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total  Category",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Active Sub-Category",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
        
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        image = request.data.get('image')
        image_file = None
        
        if request.data.get('image') or image == []:
            image_file = None

        if serializer.is_valid():
            name = serializer.validated_data.get('name', '')
            
            qs = self.queryset.filter(name=name)
            if qs.exists():
                return ResponseWrapper(error_msg="Category Name is Already Found", error_code=400)
            
            slug = unique_slug_generator_for_product_category(name=name) if name else None
            
            if image_file:
                path = 'category'
                banner_image = image_upload(file=image_file, path=path)
            else:
                banner_image = None
            
            instance = serializer.save(
                created_by=request.user,
                image = banner_image, 
                slug=slug
                )
            
            activity_log(instance, request, serializer)
            
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    # def category_wise_product_list(self, request, *args, **kwargs):
    #     qs = self.filter_queryset(self.get_queryset())
        
    #     page_qs = self.paginate_queryset(qs)
    #     serializer = CategoryWiseProductListSerializer(instance=page_qs, many=True)

    #     paginated_data = self.get_paginated_response(serializer.data)
        
    #     return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)