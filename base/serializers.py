from rest_framework import serializers
from base.models import *
from human_resource_management.models.employee import EmployeeInformation
from user.models import UserInformation
from user.serializers import BaseSerializer

class SubscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields = '__all__'

class CompanyTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyType
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PaymentType
        fields = '__all__'

class CompanyLiteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'slug',
            'primary_phone',
            'logo'
                  ]

class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'

class CompanyDetailsSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer(many=True)
    subscription = SubscriptionSerializer()
    company_owner = BaseSerializer()
    company_type = CompanyTypeSerializer()
    status_display = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Company
        fields = '__all__'
        


class UserInformationBaseSerializer(serializers.ModelSerializer):
    employee_info = serializers.SerializerMethodField(read_only = True)
    user_type = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = UserAccount
        fields = [
                    'id',  
                    'email',  
                    'phone',  
                    'employee_info',  
                    'user_type',  
                ]
        
    def get_employee_info(self, obj):
        employee_id = None
        name = None
        image = None
        slug = None
        employee_qs = EmployeeInformation.objects.filter(user= obj).last()
        
        if employee_qs:
            employee_id = employee_qs.employee_id
            name = employee_qs.name
            image = employee_qs.image
            slug = employee_qs.slug
            
        context = {
            'employee_id': employee_id,
            'name': name,
            'image': image,
            'slug': slug,
        }
        return context
        
    def get_user_type(self, obj):
        name = None
        slug = None
        qs = UserInformation.objects.filter(user= obj).last()
        
        if qs.user_type:
            name = qs.user_type.name
            slug = qs.user_type.slug
            
        context = {
            'name': name,
            'slug': slug,
        }
        return context
        
class EmployeeInformationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeInformation
        fields = [
                    'id',  
                    'employee_id',  
                    'name',  
                    'image',  
                    'slug'  
                ]
        
class TaxCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaxCategory
        fields = '__all__'
        
        
class DataSetFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    
class SMSMailSendLogSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True)
    type_display = serializers.CharField(source='get_type_display')
    sim_type_display = serializers.CharField(source='get_sim_type_display')
    
    class Meta:
        model = SMSMailSendLog
        fields = '__all__'
        
class UserNotificationSerializer(serializers.ModelSerializer):
    created_by = BaseSerializer(read_only = True)
    updated_by = BaseSerializer(read_only = True) 
    
    class Meta:
        model = UserNotification
        fields = '__all__'