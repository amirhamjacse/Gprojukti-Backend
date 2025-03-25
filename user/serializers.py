from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from human_resource_management.models.employee import Department
from user.models import UserAccount, UserType, UserInformation, UserGroup, CustomPermission
from human_resource_management.models import EmployeeInformation
User = get_user_model
from django.db.models import Q
        
class BaseSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = UserAccount
        fields = [
            'id',
            'email',
            'phone',
            'is_active',
            'user_details'
        ]
        
    def get_user_details(self, obj):
        name = '-'
        profile_pic = settings.NOT_FOUND_IMAGE
        
        user_information_qs = UserInformation.objects.filter(user = obj).last()
        if user_information_qs:
            name = user_information_qs.name
            if user_information_qs.image:
                profile_pic = user_information_qs.image
        
        context = {
            'name':name,
            'profile_pic':profile_pic,
        }
        
        return context
        
        
class CustomPermissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomPermission
        fields = '__all__'
        
class UserGroupListSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = UserGroup
        fields = [
            'id',
            'name',
            'user_details'
            ]
        
    def get_user_details(self, obj):
        total_user = 0
        user_image_list = []
        user_name_list = []
        
        user_qs = UserAccount.objects.filter(groups__name = obj.name)
        if user_qs:
            total_user = user_qs.count()
            user_image_list = user_qs.values_list('user_informations__image', 'user_informations__user__email') 
            
        context = {
            'total_user':total_user,
            'user_image_list':user_image_list 
        }
        
        return context
        
class UserGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserGroup
        fields = [
            'id',
            'name',
            'custom_permission'
                  ]
        
    def to_representation(self, instance):
        self.fields["custom_permission"] = CustomPermissionSerializer(many=True, read_only=True)
        return super(UserGroupSerializer, self).to_representation(instance)
    
        
class UserTypeSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    created_by = serializers.IntegerField(read_only=True)
    updated_by = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserType
        fields = '__all__'
       
    def to_representation(self, instance):
        self.fields["created_by"] = BaseSerializer(read_only=True)
        self.fields["updated_by"] = BaseSerializer(read_only=True)
        return super(UserTypeSerializer, self).to_representation(instance)
    
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    slug = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'slug',
            'email',
            'phone',
            'is_superuser',
            'is_active',
            'date_joined',
            'last_login',
            'password',
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def get_slug(self, obj):
        slug = '-'
        if obj:
            employee_qs = EmployeeInformation.objects.filter(
                user = obj
            ).last()
            if employee_qs:
                slug = employee_qs.slug
                
        return slug

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'user_type',
            'password',
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
class CustomerUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    otp = serializers.CharField(write_only=True) 
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone', 
            'otp', 
            'password',
                  ]
        
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class UserGoogleRegisterSerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)
class UserCaptchaRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    captcha_value = serializers.CharField(write_only=True)
    
class UserUpdateSerializer(serializers.ModelSerializer):
    user_type = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'user_type',
            'is_active'
                  ]
        
class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required = False)
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'address',
                  ]
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PasswordUpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)
    
class UserInformationListSerializer(serializers.ModelSerializer):
    groups_details = serializers.SerializerMethodField(read_only = True)
    image = serializers.SerializerMethodField(read_only = True)
    total_order = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = UserInformation
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'total_order',
            'user',
            'groups_details'
                  ]
            
    def to_representation(self, instance):
        self.fields["user"] = BaseSerializer(read_only=True)
        return super(UserInformationListSerializer, self).to_representation(instance)
    
    def get_image(self, obj):
        image = settings.NOT_FOUND_IMAGE
        
        if obj.image:
            image = obj.image
        
        return image
    
    def get_groups_details(self, obj):
        id = None
        name = None
        if obj.user:
            if obj.user.groups.last():
                id = obj.user.groups.last().id
                name = obj.user.groups.last().name
        context = {
            'id': id,
            'name': name
        }
        return context
    
    def get_total_order(self, obj):
        total_order =54
        return total_order
    
class UserInformationSerializer(serializers.ModelSerializer):
    groups_details = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = UserInformation
        fields = [
            'id',
            'name',
            'image',
            'remarks',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
            'user',
            'groups_details',
            'user_type',
                  ]
        
    def to_representation(self, instance):
        self.fields["user"] = BaseSerializer(read_only=True)
        self.fields["user_type"] = UserTypeSerializer(read_only=True)
        return super(UserInformationSerializer, self).to_representation(instance)
    
        
    def get_groups_details(self, obj):
        id = None
        name = None
        if obj.user:
            if obj.user.groups.last():
                id = obj.user.groups.last().id
                name = obj.user.groups.last().name
        context = {
            'id': id,
            'name': name
        }
        return context
    
class UserDetailsSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField(read_only = True)
    first_name = serializers.SerializerMethodField(read_only = True)
    last_name = serializers.SerializerMethodField(read_only = True)
    name = serializers.SerializerMethodField(read_only = True)
    address = serializers.SerializerMethodField(read_only = True)
    image = serializers.SerializerMethodField(read_only = True)
    employee_id = serializers.SerializerMethodField(read_only = True)
    employee_slug = serializers.SerializerMethodField(read_only = True)
    office_location = serializers.SerializerMethodField(read_only = True)
    user_type = serializers.SerializerMethodField(read_only = True)
    is_shop = serializers.SerializerMethodField(read_only = True)
    is_aic_ric_tl = serializers.SerializerMethodField(read_only = True)
    is_warehouse_manager = serializers.SerializerMethodField(read_only = True)
    is_service_center = serializers.SerializerMethodField(read_only = True)
    is_cre= serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'name',
            'image',
            'address',
            'employee_id',
            'employee_slug',
            'office_location',
            'email',
            'phone',
            'company',
            'is_superuser',
            'is_shop',
            'is_aic_ric_tl',
            'is_warehouse_manager',
            'is_service_center',
            'is_cre',
            'is_active',
            'user_type',
                  ]
    
    def get_office_location(self, obj):
        context = {}
        id = None
        name = None
        slug = None
        slug = '-'
        office_type = None
        area_slug = None
        is_use_scanner = True
        
        
        employee_qs = EmployeeInformation.objects.filter(user = obj).last()
        if employee_qs:
            if employee_qs.work_station:
                id = employee_qs.work_station.id
                name = employee_qs.work_station.name
                slug = employee_qs.work_station.slug
                office_type = employee_qs.work_station.office_type
                
                if employee_qs.user.is_superuser == True:
                    is_use_scanner = False
                    
                else:
                    is_use_scanner = employee_qs.work_station.is_use_scanner
                
                if  employee_qs.work_station.area:
                    area_slug = employee_qs.work_station.area.slug
        
        context = {
            'id':id,
            'name':name,
            'slug':slug,
            'office_type':office_type,
            'area_slug':area_slug,
            'is_use_scanner':is_use_scanner,
        }
        return context
    
    def get_name(self, obj):
        name = '-'
        employee_qs = EmployeeInformation.objects.filter(user__email = obj.email).last()
        
        if employee_qs:
            name = employee_qs.name
        
        else:
            if obj.first_name and obj.last_name:
                name =f"{obj.first_name} {obj.last_name}"
            
        return name
    
    def get_first_name(self, obj):
        name = '-'
        employee_qs = EmployeeInformation.objects.filter(user__email = obj.email).last()
        
        if employee_qs:
            name = employee_qs.name
        
        else:
            if obj.first_name and obj.last_name:
                name =f"{obj.first_name} {obj.last_name}"
            
        return name
    
    def get_last_name(self, obj):
        name = ''
            
        return name
    
    def get_is_aic_ric_tl(self, obj):
        is_aic_ric_tl = False 
        if obj.user_informations.user_type:
            if obj.user_informations.user_type.name in ['AIC', 'RIC', 'RIC TL', 'RIC-TL']:
                is_aic_ric_tl = True
                
        return is_aic_ric_tl
    
    def get_is_warehouse_manager(self, obj):
        is_warehouse_manager = False 
        if obj.user_informations.user_type:
            if obj.user_informations.user_type.name in ['Warehouse Manager', ' Warehouse Manager']:
                is_warehouse_manager = True
                
        return is_warehouse_manager
    
    def get_is_service_center(self, obj):
        is_service_center = False 
        if obj.user_informations.user_type:
            if obj.user_informations.user_type.name == 'Service Center':
                is_service_center = True
                
        return is_service_center
    
    def get_is_cre(self, obj):
        is_cre = False 
        if obj.user_informations.user_type:
            if obj.user_informations.user_type.name == 'CRE':
                is_cre = True
                
        return is_cre
    
    def get_is_shop(self, obj):
        is_shop = False 
        if obj.user_informations.user_type:
            if obj.user_informations.user_type.name == 'Shop':
                is_shop = True
            elif obj.user_informations.user_type.name == 'Shop User':
                is_shop = True
                
        return is_shop
    
    def get_user_type(self, obj):
        id = '-'
        name = '-'
        if obj.user_informations.user_type:
            id = obj.user_informations.user_type.id
            name = obj.user_informations.user_type.name 
            
        context = {
            'id': id,
            'name': name,
        }
        return context
    
    def get_employee_id(self, obj):
        employee_id = '-'
        
        employee_information_qs = EmployeeInformation.objects.filter(user__email = obj.email).last()
        if employee_information_qs:
            employee_id = employee_information_qs.employee_id
          
        return employee_id

    def get_employee_slug(self, obj):
        employee_slug = None
        
        employee_information_qs = EmployeeInformation.objects.filter(user__email = obj.email).last()
        if employee_information_qs:
            employee_slug = employee_information_qs.slug

        return employee_slug
    
    def get_address(self, obj):
        address = None
        
        qs = UserInformation.objects.filter(user = obj).last()
        if qs:
            address = qs.address
          
        return address
    
    def get_image(self, obj):
        image = settings.NOT_FOUND_IMAGE
        
        if obj.user_informations.image:
            image =obj.user_informations.image
            
        return image
    
    # def get_team_details(self, obj):
    #     total_team_member = 0
    #     context = {
    #         "total_team_member":total_team_member
            
    #     }
    #     employee_qs = EmployeeInformation.objects.filter(Q(user__email = obj.email) or Q(user__phone = obj.phone)).last()
    #     if employee_qs:
    #         if employee_qs.designations:
    #             employee_designations_name = employee_qs.designations.name
    #             employee_department_name = employee_qs.designations.departments.name
    #             company_name = employee_qs.employee_company.name
                
    #             employee_department_qs = Department.objects.filter(name = employee_department_name, designations__employee_informations__employee_company__name = company_name)
                
    #             total_team_member = employee_department_qs.count()
                
    #             context = {
    #                 "designations_name":employee_designations_name,
    #                 "department_name":employee_department_name,
    #                 "total_team_member":total_team_member
                
    #             }
        
    #     return context
    
    def get_company(self, obj):
        company_name = None
        employee_qs = EmployeeInformation.objects.filter(Q(user__email = obj.email) or Q(user__phone = obj.phone)).last()
        if employee_qs:
            if employee_qs.employee_company:
                company_name = employee_qs.employee_company.name
        return company_name
    
    # def get_overview_details(self, obj):
    #     context = {
    #         'total_compiled_task':40,
    #         'total_connection':34,
    #         'total_project_complied':134,
    #     }
    #     return context
            
    
class CustomerProfileDetailsSerializer(serializers.ModelSerializer):
    groups_details = serializers.SerializerMethodField(read_only = True)
    name = serializers.SerializerMethodField(read_only = True)
    address = serializers.SerializerMethodField(read_only = True)
    image = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'first_name',
            'last_name',
            'name',
            'image',
            'address',
            'email',
            'phone',
            'date_joined',
            'last_login',
            'groups_details',
            'is_active',
                  ]
    
    def get_name(self, obj):
        name = '-'
        
        if obj.first_name and obj.last_name:
            name =f"{obj.first_name} {obj.last_name}"
        return name
    
    def get_image(self, obj):
        image = None
        
        if obj.user_informations:
            image =obj.user_informations.image
            
        return image
    
    def get_address(self, obj):
        address = None
        
        if obj.user_informations:
            address =obj.user_informations.address
            
        return address
    
    def get_groups_details(self, obj):
        id = None
        name = None
        
        if obj.groups:
            if obj.groups.last():
                id = obj.groups.last().id
                name = obj.groups.last().name
        context = {
            'id': id,
            'name': name
        }
        return context

        
        
class UserPermissionDetailsSerializer(serializers.ModelSerializer):
    custom_permission = serializers.SerializerMethodField()
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'email',
            'phone',
            'custom_permission',
                  ]
        
    def get_custom_permission(self, obj):
        
        custom_permission = []
        
        user_group_name = "Employee"
        
        
        if obj.is_superuser == True:
            custom_permission = CustomPermission.objects.filter(is_active = True)
            serializer = CustomPermissionSerializer(custom_permission, many = True)
            return serializer.data
        
        
        if obj.user_informations:
            if obj.user_informations.user_type:
                user_type_name = obj.user_informations.user_type.name
        
        if obj.groups.count() > 1:
            
            user_type_qs = obj.groups.exclude(
                name__in = ["Customer", "Employee"]
            ).last()
            
            if user_type_qs:
                try:
                    user_type_name = user_type_qs.name
                except:
                    pass
                
            else:
                user_type_qs = obj.groups.filter(
                name__in = ["Employee"]
            ).last()
        
        if obj.groups:
            
            user_group_qs = obj.groups.filter(name__icontains = user_type_name).last()
            
            try:
                custom_permission = CustomPermission.objects.filter(user_groups__name = user_group_qs.name)
                
            except:
                custom_permission = CustomPermission.objects.filter()
            
            serializer = CustomPermissionSerializer(custom_permission, many = True)
            return serializer.data
        
        elif obj.custom_permission:
            custom_permission = obj.custom_permission.filter(user_groups__name__icontains = user_group_name)
            
            serializer = CustomPermissionSerializer(custom_permission, many = True)
            return serializer.data
        
        return custom_permission

class UserPermissionAddRemoveUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserGroup
        fields = [
            'custom_permission'
                  ]
    
class UserGroupCreateUpdateSerializer(serializers.ModelSerializer):
    is_all_permission = serializers.BooleanField(default=False, write_only=True)
    
    class Meta:
        model = UserGroup
        fields = [
            'id',
            'name',
            'custom_permission',
            'is_all_permission'
                  ]



class PermissionAddInUserSerializer(serializers.Serializer):
    employee_slug = serializers.CharField()
    

class UserInformationDownloadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = UserInformation
        fields = [
            'id',
            'name',
        ]