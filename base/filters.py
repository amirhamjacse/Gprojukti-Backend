from datetime import datetime
import django_filters
from base.models import *
from django.db.models import Q


class SubscriptionFilter(django_filters.FilterSet):
    plan = django_filters.CharFilter(label="plan",
                                         method="filter_model")
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")

    class Meta:
        model = Subscription
        fields = (
            'plan',
            'name',
            'start_date',
            'end_date',
            )

    def filter_model(self, queryset, name, value):
        plan = self.data.get('plan')
        name = self.data.get('name')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        
        if plan:
            queryset = queryset.filter(
                plan__icontains = plan
            )
        if name:
            queryset = queryset.filter(
                name__icontains = name
            )
        if start_date and end_date:
            queryset = queryset.filter(
                Q(start_date = start_date) and Q(end_date=end_date)
            )
        return queryset


class CompanyTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")

    class Meta:
        model = CompanyType
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


class PaymentTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")

    class Meta:
        model = PaymentType
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


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="name",
                                         method="filter_model")
    status = django_filters.CharFilter(label="status",
                                         method="filter_model")

    class Meta:
        model = Company
        fields = (
            'name',
            'status',
            )

    def filter_model(self, queryset, name, value):
        name = self.data.get('name')
        status = self.data.get('status')
        
        if name:
            queryset = queryset.filter(
                name__icontains = name
            )
        if status:
            queryset = queryset.filter(
                status = status
            )
        return queryset

class SMSMailSendLogFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    type = django_filters.CharFilter(label="type",
                                         method="filter_model")
    sim_type = django_filters.CharFilter(label="sim_type",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")

    class Meta:
        model = SMSMailSendLog
        fields = (
            'search',
            'type',
            'sim_type',
            'start_date',
            'end_date',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search')
        type = self.data.get('type')
        sim_type = self.data.get('sim_type')
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains = search)
                | Q(subject__icontains = search)
                | Q(body__icontains = search)
                | Q(ip_address__icontains = search)
                
            )
            
        if type:
            queryset = queryset.filter(
                type = type
            )
            
        if sim_type:
            queryset = queryset.filter(
                sim_type = sim_type
            )
            
        if start_date and end_date:
            start_date_str = start_date
            end_date_str = end_date
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            queryset = queryset.filter(
                created_at__date__range=(start_date, end_date)
            )
            
        return queryset

class UserNotificationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="search",
                                         method="filter_model")
    start_date = django_filters.CharFilter(label="start_date",
                                         method="filter_model")
    end_date = django_filters.CharFilter(label="end_date",
                                         method="filter_model")

    class Meta:
        model = UserNotification
        fields = (
            'search', 
            'start_date',
            'end_date',
            )

    def filter_model(self, queryset, name, value):
        search = self.data.get('search') 
        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains = search)
                | Q(description__icontains = search)
                | Q(user_information__email__icontains = search)
                | Q(user_information__phone__icontains = search)
                | Q(user_information__first_name__icontains = search)
                | Q(user_information__last_name__icontains = search)        
            )
            
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__date__range = (start_date, end_date)
            )
            
            
        return queryset