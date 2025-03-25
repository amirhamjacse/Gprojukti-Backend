import django_filters
from product_management.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone

class CategoryGroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")

    class Meta:
        model = CategoryGroup
        fields = (
            'name',
            )

    def filter_model(self, queryset, name, value):
        name = self.data.get('name')
        
        if name:
            queryset = queryset.filter(
                Q(name__icontains = name)
                | Q(slug__icontains = name)
                
            )
        return queryset


class CategoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")
    category = django_filters.CharFilter(label="category",
                                         method="filter_model")
    sub_category = django_filters.CharFilter(label="sub_category",
                                         method="filter_model")
    is_category = django_filters.CharFilter(label="is_category",
                                         method="filter_model")
    is_sub_category = django_filters.CharFilter(label="is_sub_category",
                                         method="filter_model")
    is_for_pc_builder = django_filters.CharFilter(label="is_for_pc_builder",
                                         method="filter_model")
    is_featured = django_filters.CharFilter(label="is_featured",
                                         method="filter_model")

    class Meta:
        model = Category
        fields = (
            'search',
            'name',
            'status',
            'category',
            'sub_category',
            'is_category',
            'is_sub_category',
            'is_featured',
            'is_for_pc_builder',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        name = self.data.get('name')
        status = self.data.get('status')
        category = self.data.get('category')
        sub_category = self.data.get('sub_category')
        is_category = self.data.get('is_category')
        is_sub_category = self.data.get('is_sub_category')
        is_for_pc_builder = self.data.get('is_for_pc_builder')
        is_featured = self.data.get('is_featured')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                
            )
        if name:
            queryset = queryset.filter(
                Q(name__icontains = name)
                | Q(slug__icontains = name)
                
            )
        if status:
            queryset = queryset.filter(
                Q(status = status)
            )
        if category:
            if category.lower() == 'true' :
                queryset = queryset.filter(
                    Q(status = 'STANDALONE')
                    | Q(status = 'PARENT')
                    
                )
        if sub_category:
            if sub_category.lower() == 'true' :
                queryset = queryset.filter(
                    Q(status = 'CHILD')
                    | Q(status = 'CHILD_OF_CHILD')                    
                )
                
        if is_category:
            if is_category.lower() == 'true' :
                queryset = queryset.filter(
                    Q(status = 'STANDALONE')
                    | Q(status = 'PARENT')
                    
                )
        if is_sub_category:
            if is_sub_category.lower() == 'true' :
                queryset = queryset.filter(
                    Q(status = 'CHILD')
                    | Q(status = 'CHILD_OF_CHILD')                    
                )
                
        if is_for_pc_builder:
            if is_for_pc_builder.lower() == 'true' :
                queryset = queryset.filter(
                    is_for_pc_builder = True                    
                )
            elif is_for_pc_builder.lower() == 'false' :
                queryset = queryset.filter(
                    is_for_pc_builder = False                    
                )
                
        if is_featured:
            if is_featured.lower() == 'true' :
                queryset = queryset.filter(
                    is_featured = True                    
                )
            elif is_featured.lower() == 'false' :
                queryset = queryset.filter(
                    is_featured = False                    
                )
                
        return queryset
    
