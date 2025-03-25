from django.db.models import Q
from base.filters import *
from product_management.filter.category import CategoryFilter
from product_management.serializers.category import *
from product_management.models import Category, CategoryGroup
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from utils.permissions import *
import re
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PublicCategoryGroupViewSet(CustomViewSet):
    queryset = CategoryGroup.objects.all().filter(is_active = True, is_featured = True)
    lookup_field = 'pk'
    serializer_class = CategoryGroupListSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["list"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['list']:
            self.serializer_class = CategoryGroupListSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = CategoryGroupSerializer
        else:
            self.serializer_class = CategoryGroupListSerializer
            
        return self.serializer_class
    

class PublicCategoryViewSet(CustomViewSet):
    queryset = Category.objects.all().filter(status__in = ['STANDALONE', 'PARENT','CHILD'], 
                                             is_active = True)
    lookup_field = 'slug'
    serializer_class = PublicCategoryListSerializer
    permission_classes = [AllowAny]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CategoryFilter
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['list']:
            self.serializer_class = PublicCategoryListSerializer
        elif self.action in ['retrieve']:
            self.serializer_class = CategorySerializer
        else:
            self.serializer_class = PublicCategoryListSerializer
            
        return self.serializer_class
