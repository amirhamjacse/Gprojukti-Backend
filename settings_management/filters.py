import django_filters
from settings_management.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone

class SliderFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")
    is_popup = django_filters.CharFilter(label="is_popup",
                                         method="filter_model")
    is_slider = django_filters.CharFilter(label="is_slider",
                                         method="filter_model")

    class Meta:
        model = Slider
        fields = (
            'search', 
            'is_active', 
            'is_slider', 
            'is_popup', 
            )

    def filter_model(self, queryset, name, value):
        name = self.data.get('name')
        is_active = self.data.get('is_active')
        is_popup = self.data.get('is_popup')
        is_slider = self.data.get('is_slider')
        
        if name:
            queryset = queryset.filter(
                Q(name__icontains = name)
                | Q(codename__icontains = name)
            )
        
        if is_active:
            if is_active.lower() == 'true':
                queryset = queryset.filter(
                    is_active=True
                    )
            
            if is_active.lower() == 'false':
                queryset = queryset.filter(
                    is_active=False
                    )
        
        if is_slider:
            if is_slider.lower() == 'true':
                queryset = queryset.filter(
                    is_slider=True
                    )
            
            if is_slider.lower() == 'false':
                queryset = queryset.filter(
                    is_slider=False
                    )
        
        if is_popup:
            if is_popup.lower() == 'true':
                queryset = queryset.filter(
                    is_popup=True
                    )
            
            if is_popup.lower() == 'false':
                queryset = queryset.filter(
                    is_popup=False
                    )
            
        return queryset


class ShopDayEndFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    shop = django_filters.CharFilter(label="shop",
                                         method="filter_model")

    class Meta:
        model = ShopDayEnd
        fields = (
            'search', 
            'start_date', 
            'end_date', 
            'shop', 
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        shop = self.data.get('shop')
        
        if search:
            queryset = queryset.filter(
                Q(shop__name__icontains = search)
                | Q(shop__slug__icontains = search)
                | Q(id__icontains = search)
            )
        
        if start_date and end_date:
            queryset = queryset.filter(
                day_end_date__date__range = (start_date, end_date)
                )
        if shop:
            queryset = queryset.filter(
                Q(shop__name__icontains = shop)
                | Q(shop__slug__icontains = shop)
            )
            
        return queryset
