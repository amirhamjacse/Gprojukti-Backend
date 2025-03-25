import django_filters
from location.models import *
from django_filters.rest_framework import FilterSet
from django.db.models import Count, Min, Q
from datetime import date, datetime, timedelta
from django.utils import timezone

class OfficeLocationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    office_type = django_filters.CharFilter(label="office_type",
                                         method="filter_model")
    company = django_filters.CharFilter(label="company",
                                         method="filter_model")
    is_shown_in_website = django_filters.CharFilter(label="is_shown_in_website",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = OfficeLocation
        fields = (
            'search',
            'office_type',
            'company',
            'is_shown_in_website',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        office_type = self.data.get('office_type')
        company = self.data.get('company')
        is_shown_in_website = self.data.get('is_shown_in_website')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(bn_name__icontains = search)
                | Q(primary_phone__icontains = search)
            )
            
        if office_type:
            queryset = queryset.filter(
                office_type = office_type
            )
            
        if company:
            queryset = queryset.filter(
                Q(name__icontains = company)
                | Q(slug__icontains = company)
            )
            
        if is_shown_in_website:
            if is_shown_in_website.lower() == 'true' :
                queryset = queryset.filter(
                    is_shown_in_website = True 
                )
            else:
                queryset = queryset.filter(
                    is_shown_in_website = False 
                )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
        return queryset


class DivisionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = Division
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
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
        return queryset
    
class DistrictFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")
    division = django_filters.CharFilter(label="division",
                                         method="filter_model")
    area = django_filters.CharFilter(label="area",
                                         method="filter_model")

    class Meta:
        model = District
        fields = (
            'search',
            'division',
            'area',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        division = self.data.get('division')
        is_active = self.data.get('is_active')
        area = self.data.get('area')
        
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
            )
            
        if area:
            queryset = queryset.filter(
                Q(areas__name__icontains = area)
                | Q(areas__slug__icontains = area)
            ).distinct()
            
        if division:
            queryset = queryset.filter(
                Q(division__name__icontains = division)
                | Q(division__slug__icontains = division)
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset


    
class AreaFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")
    district = django_filters.CharFilter(label="district",
                                         method="filter_model")

    class Meta:
        model = Area
        fields = (
            'search',
            'district',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        district = self.data.get('district')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
            )
            
        if district:
            queryset = queryset.filter(
                Q(district__name__icontains = district)
                | Q(district__slug__icontains = district)
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset


class POSAreaFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    area = django_filters.CharFilter(label="area",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = POSArea
        fields = (
            'search',
            'area',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        area = self.data.get('area')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(bn_name__icontains = search)
            )
            
        if area:
            queryset = queryset.filter(
                Q(area__name__icontains = area)
                | Q(area__slug__icontains = area)
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset


class POSRegionFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    pos_area = django_filters.CharFilter(label="pos_area",
                                         method="filter_model")
    is_active = django_filters.CharFilter(label="is_active",
                                         method="filter_model")

    class Meta:
        model = POSRegion
        fields = (
            'search',
            'pos_area',
            'is_active',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        pos_area = self.data.get('pos_area')
        is_active = self.data.get('is_active')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains = search)
                | Q(slug__icontains = search)
                | Q(bn_name__icontains = search)
            )
            
        if pos_area:
            queryset = queryset.filter(
                Q(pos_area__name__icontains = pos_area)
                | Q(pos_area__slug__icontains = pos_area)
            )
            
        if is_active:
            if is_active.lower() == 'true' :
                queryset = queryset.filter(
                    is_active = True 
                )
            else:
                queryset = queryset.filter(
                    is_active = False 
                )
                
        return queryset

