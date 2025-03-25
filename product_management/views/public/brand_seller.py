from django.db.models import Q
from base.filters import *
from product_management.filter.brand_seller import BrandFilter
from product_management.serializers.brand_seller import *
from product_management.models import Brand
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from utils.permissions import *
import re
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PublicBrandViewSet(CustomViewSet):
    queryset = Brand.objects.all()
    lookup_field = 'pk'
    serializer_class = BrandListSerializer
    permission_classes = [AllowAny]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = BrandFilter
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["list"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
