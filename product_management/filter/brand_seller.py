import django_filters
from product_management.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone


class BrandFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_featured = django_filters.CharFilter(label="is_featured",
                                         method="filter_model")
    is_show_in_ecommece = django_filters.CharFilter(label="is_show_in_ecommece",
                                         method="filter_model")
    is_show_in_pos = django_filters.CharFilter(label="is_show_in_pos",
                                         method="filter_model")
    category = django_filters.CharFilter(label="category",
                                         method="filter_model")

    class Meta:
        model = Brand
        fields = (
            'search',
            'is_featured',
            'is_show_in_ecommece',
            'is_show_in_pos',
            'category',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        is_featured = self.data.get('is_featured')
        is_show_in_ecommece = self.data.get('is_show_in_ecommece')
        is_show_in_pos = self.data.get('is_show_in_pos')
        category = self.data.get('category')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                
            )
            
        if is_featured:
            if is_featured.lower() == 'true' :
                queryset = queryset.filter(
                    Q(is_featured = True)
                )
            elif is_featured.lower() == 'false' :
                queryset = queryset.filter(
                    Q(is_featured = False)
                )
            
        if is_show_in_ecommece:
            if is_show_in_ecommece.lower() == 'true' :
                queryset = queryset.filter(
                    Q(is_show_in_ecommece = True)
                )
            elif is_show_in_ecommece.lower() == 'false' :
                queryset = queryset.filter(
                    Q(is_show_in_ecommece = False)
                )
            
        if category:
            queryset = queryset.filter(
                Q(products__category__name__icontains = category)
                | Q(products__category__slug__icontains = category)
                | Q(products__sub_category__slug__icontains = category)
                | Q(products__sub_category__name__icontains = category)
                # | Q(products__category__slug__icontains = category)
                # | Q(products__sub_category__name__icontains = category)
                # | Q(products__sub_category__slug__icontains = category)
            ).distinct()
            
        if is_show_in_pos:
            if is_show_in_pos.lower() == 'true' :
                queryset = queryset.filter(
                    Q(is_show_in_pos = True)
                )
            elif is_show_in_pos.lower() == 'false' :
                queryset = queryset.filter(
                    Q(is_show_in_pos = False)
                )
        return queryset
    
    
class SupplierFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = Supplier
        fields = (
            'search',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    Q(is_active = True)
                )
            elif is_active.lower() == 'false' :
                queryset = queryset.filter(
                    Q(is_active = False)
                )
            
        return queryset   
     
class SellerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")
    is_show_in_ecommece = django_filters.CharFilter(label="is_show_in_ecommece",
                                         method="filter_model")
    is_show_in_pos = django_filters.CharFilter(label="is_show_in_pos",
                                         method="filter_model")

    class Meta:
        model = Seller
        fields = (
            'search',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    Q(is_active = True)
                )
            elif is_active.lower() == 'false' :
                queryset = queryset.filter(
                    Q(is_active = False)
                )
                
        return queryset