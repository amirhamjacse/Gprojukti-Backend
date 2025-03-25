import django_filters
from user.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone

from user_activity.models import ActivityLog

class ActivityLogFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    employee = django_filters.CharFilter(label="employee",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")
    method = django_filters.CharFilter(label="method",
                                         method="filter_model")

    class Meta:
        model = ActivityLog
        fields = (
            'search', 
            'employee', 
            'start_date', 
            'end_date',
            'method',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        employee = self.data.get('employee')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        method = self.data.get('method')
        
        if search:
            queryset = queryset.filter(
                Q(actor__email__icontains = search)
                | Q(ip_address__icontains = search)
                | Q(request_url__icontains = search)
                | Q(actor__email__icontains = search)
                | Q(actor__first_name__icontains = search)
                | Q(actor__last_name__icontains = search)
            ) 
        
        if employee:
            queryset = queryset.filter(
                Q(actor__employee_informations__employee_id__icontains = employee)
                | Q(actor__employee_informations__name__icontains = employee)
                | Q(actor__employee_informations__nid_number__icontains = employee)
                | Q(actor__email__icontains = employee)
            ) 
        
        if start_date and end_date: 
            queryset = queryset.filter(
                action_time__date__range = (start_date, end_date)
            )
            
        
        if method: 
            queryset = queryset.filter(
                action_type__icontains = method
                )   
            
        queryset = queryset.distinct()
        
        return queryset

