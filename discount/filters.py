import django_filters
from discount.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone


class DiscountFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    start_time = django_filters.CharFilter(label="start_time",
                                         method="filter_model")
    end_time = django_filters.CharFilter(label="end_time",
                                         method="filter_model")
    schedule_type = django_filters.CharFilter(label="schedule_type",
                                         method="filter_model")
    discount_type = django_filters.CharFilter(label="discount_type",
                                         method="filter_model")
    discount_status = django_filters.CharFilter(label="discount_status",
                                         method="filter_model")

    class Meta:
        model = Discount
        fields = (
            'search',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'discount_type',
            'discount_status',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')
        schedule_type = self.data.get('schedule_type')
        discount_type = self.data.get('discount_type')
        discount_status = self.data.get('discount_status')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(description__icontains = search)
            )
            
        if discount_status:
            queryset = queryset.filter(
                discount_status = discount_status
            )
            
        if discount_type:
            queryset = queryset.filter(
                discount_type = discount_type
            )
            
        if schedule_type:
            queryset = queryset.filter(
                schedule_type = schedule_type
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                Q(start_date__gte = start_date) 
                & Q(end_date__lte = end_date) 
                & Q(schedule_type = 'DATE_WISE') 
            )
            
        if start_time and end_time:
            queryset = queryset.filter(
                Q(start_time__gte = start_time) 
                & Q(end_time__lte = end_time) 
                & Q(schedule_type = 'TIME_WISE') 
            )
            
        return queryset
    
    
class PromoCodeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    start_time = django_filters.CharFilter(label="start_time",
                                         method="filter_model")
    end_time = django_filters.CharFilter(label="end_time",
                                         method="filter_model")
    schedule_type = django_filters.CharFilter(label="schedule_type",
                                         method="filter_model")
    promo_type = django_filters.CharFilter(label="promo_type",
                                         method="filter_model")

    class Meta:
        model = PromoCode
        fields = (
            'search',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'schedule_type',
            'promo_type',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')
        schedule_type = self.data.get('schedule_type')
        promo_type = self.data.get('promo_type')
        
        if search:
            queryset = queryset.filter(
                Q(promo_code__icontains = search)
                | Q(slug__icontains = search)
            )
            
        if promo_type:
            queryset = queryset.filter(
                promo_type = promo_type
            )
            
        if schedule_type:
            queryset = queryset.filter(
                schedule_type = schedule_type
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                Q(start_date__gte = start_date) 
                & Q(end_date__lte = end_date) 
                & Q(schedule_type = 'DATE_WISE') 
            )
            
        if start_time and end_time:
            queryset = queryset.filter(
                Q(start_time__gte = start_time) 
                & Q(end_time__lte = end_time) 
                & Q(schedule_type = 'TIME_WISE') 
            )
            
        return queryset
