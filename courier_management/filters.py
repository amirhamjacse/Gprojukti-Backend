import django_filters
from courier_management.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone
from datetime import datetime


class CourierServiceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")

    class Meta:
        model = CourierService
        fields = (
            'search',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(email__icontains = search)
                | Q(phone__icontains = search)
                | Q(address__icontains = search)
            )
        return queryset
   
    


class DeliveryManFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")

    class Meta:
        model = DeliveryMan
        fields = (
            'search',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(email__icontains = search)
                | Q(phone__icontains = search)
                | Q(employee__employee_id__icontains = search)
            )
        return queryset
   
    