from django.db.models import Q
from base.filters import *
from discount.models import Discount
from discount.serializers import DiscountListSerializer, DiscountWiseProductListSerializer
from gporjukti_backend_v2.settings import CURRENT_TIME, TODAY
from human_resource_management.models.employee import EmployeeInformation
from location.models import OfficeLocation
from location.serializers import OfficeLocationListSerializer
from product_management.filter.product import ProductFilter
from product_management.serializers.product import *
from product_management.models import Product
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from utils.permissions import *
import re
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PublicProductViewSet(CustomViewSet):
    queryset = Product.objects.filter(is_active = True).order_by('is_cart_disabled')
    
    # queryset = Product.objects.all().filter(is_active = True)
    lookup_field = 'pk'
    serializer_class = PublicProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ProductFilter 
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["list", "retrieve", "active_deals_of_week_product_list", "active_campaign_product_list"]:
            permission_classes = [permissions.AllowAny]
        if self.action in ["product_review"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['list']:
            self.serializer_class = PublicProductListSerializer
        elif self.action in ['on_the_product_list']:
            self.serializer_class = PublicOnTheGoProductListSerializer
        elif self.action in ['product_review']:
            self.serializer_class = CustomerProductReview
        else:
            self.serializer_class = PublicProductDetailsSerializer

        return self.serializer_class
    
    def on_the_product_list(self, request, district, *args, **kwargs):
        shop  = request.GET.get('shop') 
        
        qs = Product.objects.filter(product_price_infos__product_stocks__stock_location__area__district__slug = district, product_price_infos__product_stocks__status = 'ACTIVE').distinct()
        
        qs = self.filter_queryset(qs)
        
        serializer_class = self.get_serializer_class()
        
        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200) 
    
    def on_the_product_wise_shop_list(self, request, district, product, *args, **kwargs):
        shop_qs = OfficeLocation.objects.filter(area__district__slug = district, product_stocks__product_price_info__product__slug = product).distinct()
        
        page_qs = self.paginate_queryset(shop_qs)
        serializer = OfficeLocationListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200) 
    
    def active_deals_of_week_product_list(self, request, *args, **kwargs):
        today = TODAY
        current_time = CURRENT_TIME
    
        discount_qs = Discount.objects.filter(
            Q(discount_status='DEAL_OF_WEEK', schedule_type='DATE_WISE', start_date__date__lte=today, end_date__date__gte=today) |
            Q(discount_status='DEAL_OF_WEEK', schedule_type='TIME_WISE', start_time__lte=today.time(), end_time__gte=today.time())
        )
        
        page_qs = self.paginate_queryset(discount_qs)
        serializer = DiscountWiseProductListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
    
    def active_campaign_product_list(self, request, *args, **kwargs):
        today = TODAY
        current_time = CURRENT_TIME
    
        discount_qs = Discount.objects.filter(
            Q(discount_status='CAMPAIGN', schedule_type='DATE_WISE', start_date__date__lte=today, end_date__date__gte=today) |
            Q(discount_status='CAMPAIGN', schedule_type='TIME_WISE', start_time__lte=today.time(), end_time__gte=today.time())
        )
        
        page_qs = self.paginate_queryset(discount_qs)
        serializer = DiscountListSerializer(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
    
    def product_review(self, request, product_slug, *args, **kwargs):
        product_qs = Product.objects.filter(slug = product_slug).last()
        if not product_qs:
            return ResponseWrapper(
                error_msg="Product is Not Found", error_code=404
            )
        rating = request.data.get('rating')
        review_text = request.data.get('review_text')
        order = request.data.get('order')
        
        review_qs = ProductReview.objects.create(
            rating = rating, review_text= review_text, product = product_qs,created_by = request.user
        )
        serializer = CustomerProductReview(instance=review_qs)
        
        return ResponseWrapper(data=serializer.data,  msg="Success", status=200) 
    
    def product_review_list(self, request, product_slug, *args, **kwargs):
        product_qs = Product.objects.filter(slug = product_slug).last()
        if not product_qs:
            return ResponseWrapper(
                error_msg="Product is Not Found", error_code=404
            )
            
        review_qs = ProductReview.objects.filter(
            product = product_qs
        )
        serializer = CustomerProductReview(instance=review_qs, many = True)
        
        return ResponseWrapper(data=serializer.data,  msg="Success", status=200) 

    def product_attribute_list(self, request, slug, *args, **kwargs):
        product_qs = Product.objects.filter(product_attribute_value__slug__icontains = slug)
        
        if not product_qs:
            return ResponseWrapper(
                error_msg="Product is Not Found", error_code=404
            )
             
        product_attribute_value_qs = ProductAttributeValue.objects.filter(
            product_attribute__name__icontains = 'Storage', 
            products__slug__in = product_qs.values_list('slug', flat = True)
        ).distinct('value')
        
        serializer = ProductAttributeListSerializer(instance=product_attribute_value_qs, many = True)
        
        return ResponseWrapper(data=serializer.data,  msg="Success", status=200) 
    
