import django_filters
from user.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone

class CustomPermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="name",
                                         method="filter_custom_permission")
    codename = django_filters.CharFilter(label="codename",
                                         method="filter_custom_permission")
    model_name = django_filters.CharFilter(label="model_name",
                                         method="filter_custom_permission")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_custom_permission")

    class Meta:
        model = CustomPermission
        fields = (
            'name', 
            'codename', 
            'model_name'
            )

    def filter_custom_permission(self, queryset, name, value):
        name = self.data.get('name')
        codename = self.data.get('codename')
        model_name = self.data.get('model_name')
        is_active = self.data.get('is_active')
        
        if name:
            queryset = queryset.filter(
                Q(name__icontains = name)
                | Q(codename__icontains = name)
                | Q(model_name__icontains = name)
            )
        
        if codename:
            queryset = queryset.filter(
                codename__icontains = codename
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
        
        if model_name:
            queryset = queryset.filter(
                model_name = model_name
            )
            
        return queryset

class UserGroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")

    class Meta:
        model = UserGroup
        fields = (
            'name',
            )

    def filter_model(self, queryset, name, value):
        name = self.data.get('name')
        
        if name:
            queryset = queryset.filter(
                name__icontains = name
            )
        return queryset


class UserInformationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")
    email = django_filters.CharFilter(label="email",
                                         method="filter_model")
    phone = django_filters.CharFilter(label="phone",
                                         method="filter_model")
    user_type = django_filters.CharFilter(label="user_type",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")
    division = django_filters.CharFilter(label="division",
                                         method="filter_model")
    district = django_filters.CharFilter(label="district",
                                         method="filter_model")
    area = django_filters.CharFilter(label="area",
                                         method="filter_model")

    class Meta:
        model = UserInformation
        fields = (
            'search',
            'name',
            'email',
            'phone',
            'user_type',
            'is_active',
            'division',
            'district',
            'area',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        name = self.data.get('name')
        email = self.data.get('email')
        phone = self.data.get('phone')
        user_type = self.data.get('user_type')
        is_active = self.data.get('is_active')
        division = self.data.get('division')
        district = self.data.get('district')
        area = self.data.get('area')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                |Q(user__email__icontains = search)
                |Q(user__phone__icontains = search)
                |Q(user__first_name__icontains = search)
                |Q(user__last_name__icontains = search)
                )
        
        if name:
            queryset = queryset.filter(
                Q(name__icontains = name)
                |Q(user__first_name__icontains = name)
                |Q(user__last_name__icontains = name)
                )
        
        if user_type:
            queryset = queryset.filter(
                Q(user_type__name__icontains = user_type)
                | Q(user_type__id__icontains = str(user_type))
                )
        if email:
            queryset = queryset.filter(
                user__email__icontains = email
                )
        
        if phone:
            queryset = queryset.filter(
                user__phone__icontains = phone
                )
        
        if is_active:
            queryset = queryset.filter(
                user__is_active = True
                )
            
        if division:
            queryset = queryset.filter(
                user__customer_address_log_created_bys__division_name__icontains = division
                )
            
        if district:
            queryset = queryset.filter(
                user__customer_address_log_created_bys__district_name__icontains = district
                )
        if area:
            queryset = queryset.filter(
                user__customer_address_log_created_bys__area_name__icontains = area
                )
            
        return queryset
