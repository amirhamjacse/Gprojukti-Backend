from django.db.models import Q
from Script.code.product import *
from Script.code.user import *

# import re
from base.models import *
from base.serializers import *
from base.filters import *
from human_resource_management.models.employee import *
from location.models import *
from product_management.models.category import CategoryGroup
from user.models import *
from utils.dataset import *
from utils.decorators import log_activity
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from utils.permissions import *
import re
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class DataViewSet(CustomViewSet):
    queryset = Subscription.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = SubscriptionSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SubscriptionFilter 
    
    def list(self, request,  *args, **kwargs):
        user_list = USER_LIST
        department_list = DEPARTMENT
        subscription_plan_list = SUBSCRIPTION_PLAN_LIST
        company_type_list = COMPANY_TYPE_LIST
        payment_type_list = PAYMENT_TYPE_LIST
        company_list = COMPANY_LIST
        tax_category_list = TAX_CATEGORY_LIST
        country_list = COUNTRY_LIST
        division_list = DIVISION_LIST
        district_list = DISTRICT_LIST
        area_list = AREA_LIST
        pos_area_list = POS_AREA_LIST
        pos_region_list = POS_REGION_LIST
        office_location_list = OFFICE_LOCATION_LIST
        product_list = PRODUCT_LIST
        category_product_list = CATEGORY_GROUP_LIST
        multiple_department_create = USER_GROUP_PERMISSION
        
        request_user = request.user
        
        # # Employee Create and  Update
        
        company_qs = Company.objects.filter(name__icontains = 'Gprojukti').last()
        
        # User Group
        user_group_qs = multiple_user_permission_create(multiple_department_create, request_user)
        
        # for item in category_product_list:
        #     name = item.get('name')
        #     category_image_url = item.get('category_image_url')
        #     category_list = item.get('category_list')
            
        #     slug = unique_slug_generator(name = name)
        #     qs = CategoryGroup.objects.create(
        #         name = name, slug = slug, company = company_qs,
        #         banner_image = category_image_url, created_by = request_user
        #     )
        #     for category in category_list: 
        #         category_name = category.get('name')
        #         category_image_url = category.get('category_image_url')
                
        #         category_name = f"{category_name} {name}"
        #         slug = unique_slug_generator(name = category_name)
                
        #         category_qs = Category.objects.create(
        #         name = category_name, slug = slug, status = "PARENT",
        #         banner_image = category_image_url, category_group = qs, created_by = request_user
        #     )
        
        # employee_list = multiple_employee_create(employee_list= user_list, request_user = request_user)
        
        # # Department Create and Update
        # department_list = multiple_department_create(department_list= department_list, request_user = request_user)
        
        # # Product Create and Update
        # product_list = multiple_product_create(product_list= product_list, request_user = request_user)
        
        # Product Create and Update
        # product_stock_in_list = multiple_product_stock_in_create(product_list= product_list, request_user = request_user)
        
        # Country Create and Update
        
        # for item in country_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
            
        #     country_qs = Country.objects.filter(slug = slug).last()
            
        #     if country_qs:
        #         country_qs.name = name
        #         country_qs.slug = slug
        #         country_qs.bn_name = bn_name
        #         country_qs.created_by = request_user
        #         country_qs.save()
        #     else:
        #         country_qs = Country.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        # print('Country Create Done')
        
        # # Division Create and Update
        
        # for item in division_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     country = item.get('country')
            
        #     division_qs = Division.objects.filter(name = name).last()
            
        #     if division_qs:
        #         division_qs.name = name
        #         division_qs.slug = slug
        #         division_qs.bn_name = bn_name
        #         division_qs.created_by = request_user
        #         division_qs.save()
        #     else:
        #         division_qs = Division.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        #     f_qs = Country.objects.filter(name = country).last()
            
        #     if f_qs:
        #         division_qs.country = f_qs
        #         division_qs.save()
                
        # print('Division Create Done')
        
        # # District Create and Update
        
        # for item in district_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     division = item.get('division')
            
        #     district_qs = District.objects.filter(name = name).last()
            
        #     if district_qs:
        #         district_qs.name = name
        #         district_qs.slug = slug
        #         district_qs.bn_name = bn_name
        #         district_qs.created_by = request_user
        #         district_qs.save()
        #     else:
        #         district_qs = District.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        #     f_qs = Division.objects.filter(name = division).last()
            
        #     if f_qs:
        #         district_qs.division = f_qs
        #         district_qs.save()
                
        # print('District Create Done')
        
        # Area Create and Update
        
        # for item in area_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     district = item.get('district')
            
        #     area_qs = Area.objects.filter(name = name).last()
            
        #     if area_qs:
        #         area_qs.name = name
        #         area_qs.slug = slug
        #         area_qs.bn_name = bn_name
        #         area_qs.created_by = request_user
        #         area_qs.save()
        #     else:
        #         area_qs = Area.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        #     f_qs = District.objects.filter(name = district).last()
            
        #     if f_qs:
        #         area_qs.district = f_qs
        #         area_qs.save()
                
        # print('Area Create Done')
        
        
        # POS Area Create and Update
        
        # for item in pos_area_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     area = item.get('area')
            
        #     pos_area_qs = POSArea.objects.filter(name = name).last()
            
        #     if pos_area_qs:
        #         pos_area_qs.name = name
        #         pos_area_qs.slug = slug
        #         pos_area_qs.bn_name = bn_name
        #         pos_area_qs.created_by = request_user
        #         pos_area_qs.save()
        #     else:
        #         pos_area_qs = POSArea.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        #     f_qs = Area.objects.filter(name = area).last()
            
        #     if f_qs:
        #         pos_area_qs.area = f_qs
        #         pos_area_qs.save()
                
        # print('POS Area Create Done')
        # POS Area Create and Update
        
        # for item in pos_area_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     area = item.get('area')
            
        #     pos_area_qs = POSArea.objects.filter(name = name).last()
            
        #     if pos_area_qs:
        #         pos_area_qs.name = name
        #         pos_area_qs.slug = slug
        #         pos_area_qs.bn_name = bn_name
        #         pos_area_qs.created_by = request_user
        #         pos_area_qs.save()
        #     else:
        #         pos_area_qs = POSArea.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        #     f_qs = Area.objects.filter(name = area).last()
        #     print('area', area, f_qs)
            
        #     if f_qs:
        #         pos_area_qs.area = f_qs
        #         pos_area_qs.save()
                
        # print('POS Area Create Done')
        
        
        # # POS Region Create and Update
        
        # for item in pos_region_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     pos_area = item.get('pos_area')
            
        #     qs = POSRegion.objects.filter(name = name).last()
            
        #     if qs:
        #         qs.name = name
        #         qs.slug = slug
        #         qs.bn_name = bn_name
        #         qs.created_by = request_user
        #         qs.save()
        #     else:
        #         qs = POSRegion.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             created_by = request_user
        #             )
                
        #     f_qs = POSArea.objects.filter(name = pos_area).last()
        #     print('area', qs.name, f_qs)
            
        #     if f_qs:
        #         qs.pos_area = f_qs
        #         qs.save()
                
        # print('POS Region Create Done')
        
        # POS Region Create and Update
        
        # for item in subscription_plan_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     plan = item.get('plan')
        #     plan_type = item.get('plan_type')
        #     plan_value = item.get('plan_value')
        #     category_limit = item.get('category_limit')
        #     product_limit = item.get('product_limit')
        #     employee_limit = item.get('employee_limit')
        #     shop_limit = item.get('shop_limit')
            
        #     qs = Subscription.objects.filter(name = name).last()
            
        #     if qs:
        #         qs.name = name
        #         qs.slug = slug
        #         qs.plan = plan
        #         qs.plan_type = plan_type
        #         qs.plan_value = plan_value
        #         qs.category_limit = category_limit
        #         qs.product_limit = product_limit
        #         qs.employee_limit = employee_limit
        #         qs.shop_limit = shop_limit
        #         qs.created_by = request_user
        #         qs.save()
        #     else:
        #         qs = Subscription.objects.create(
        #             name=name,
        #             slug = slug,
        #             plan = plan,
        #             plan_type = plan_type,
        #             plan_value = plan_value,
        #             category_limit = category_limit,
        #             product_limit = product_limit,
        #             employee_limit = employee_limit,
        #             shop_limit = shop_limit,
        #             created_by = request_user
        #             )
        # print('Subscription Create Done')
        
        # for item in company_type_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
            
        #     qs = CompanyType.objects.filter(name = name).last()
            
        #     if qs:
        #         qs.name = name
        #         qs.slug = slug
        #         qs.save()
        #     else:
        #         qs = CompanyType.objects.create(
        #             name=name,
        #             slug = slug,
        #             created_by = request_user
        #             )
        # print('Company Type Create Done')
        
        # for item in payment_type_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     logo = item.get('logo')
            
        #     qs = PaymentType.objects.filter(slug = slug).last()
            
        #     if qs:
        #         qs.name = name
        #         qs.slug = slug
        #         qs.logo = logo
        #         qs.save()
        #     else:
        #         qs = PaymentType.objects.create(
        #             name=name,
        #             slug = slug,
        #             logo = logo,
        #             created_by = request_user
        #             )
        # print('Payment Type Create Done')
        
        
        # for item in company_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     logo = item.get('logo')
        #     primary_phone = item.get('primary_phone')
        #     secondary_phone = item.get('secondary_phone')
        #     email = item.get('email')
        #     website_url = item.get('website_url')
        #     vat_registration_no = item.get('vat_registration_no')
        #     registration_number = item.get('registration_number')
        #     address = item.get('address')
        #     starting_date = item.get('starting_date')
        #     company_owner = item.get('company_owner')
        #     subscription = item.get('subscription')
        #     company_type = item.get('company_type')
        #     payment_type = item.get('payment_type')
        #     currency = item.get('currency')
        #     status = item.get('status')
            
        #     qs = PaymentType.objects.filter(name = name).last()
            
        #     if qs:
        #         qs.name = name
        #         qs.slug = slug
        #         qs.logo = logo
        #         qs.save()
        #     else:
        #         qs = PaymentType.objects.create(
        #             name=name,
        #             slug = slug,
        #             logo = logo,
        #             created_by = request_user
        #             )
        # print('Payment Type Create Done')
        
        
        # POS Region Create and Update
        
        # for item in office_location_list:
        #     name = item.get('name')
        #     slug = item.get('slug')
        #     bn_name = item.get('bn_name')
        #     store_no = item.get('store_no')
        #     address = item.get('address')
        #     primary_phone = item.get('primary_phone')
        #     area = item.get('area')
        #     company = item.get('company')
        #     office_type = item.get('office_type')
        #     pos_area = item.get('pos_area')
        #     is_shown_in_website = item.get('is_shown_in_website')
            
        #     qs = OfficeLocation.objects.filter(name = name).last()
        #     pos_area_qs = Area.objects.all().order_by('?').last()
            
        #     if qs:
        #         qs.name = name
        #         qs.slug = slug
        #         qs.bn_name = bn_name
        #         # qs.pos_area = pos_area_qs
        #         qs.created_by = request_user
        #         qs.save()
        #     else:
        #         qs = OfficeLocation.objects.create(
        #             name=name,
        #             slug = slug,
        #             bn_name = bn_name,
        #             store_no = store_no,
        #             address = address,
        #             primary_phone = primary_phone,
        #             # area = area,
        #             office_type = office_type,
        #             area = pos_area_qs,
        #             is_shown_in_website = True,
        #             created_by = request_user
        #             )
                
        #     f_qs = POSArea.objects.filter(name = pos_area).last()
        #     print('area', qs.name, f_qs)
            
        #     if f_qs:
        #         qs.pos_area = f_qs
        #         qs.save()
                
        # print('POS Region Create Done')

        context = {
            'user_list':user_list,
            'subscription_plan_list':subscription_plan_list,
            'company_type_list':company_type_list,
            'payment_type_list':payment_type_list,
            'company_list':company_list,
            'tax_category_list':tax_category_list,
            'country_list':country_list,
            'division_list':division_list,
            'district_list':district_list,
            'area_list':area_list,
            'pos_area_list':pos_area_list,
            'pos_region_list':pos_region_list,
        }
        
        return ResponseWrapper(data=context, msg='Success', status=200)

class SubscriptionViewSet(CustomViewSet):
    queryset = Subscription.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = SubscriptionSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SubscriptionFilter 


class CompanyTypeViewSet(CustomViewSet):
    queryset = CompanyType.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = CompanyTypeSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CompanyTypeFilter 


class PaymentTypeViewSet(CustomViewSet):
    queryset = PaymentType.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = PaymentTypeSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = PaymentTypeFilter 


class CompanyViewSet(CustomViewSet):
    queryset = Company.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = CompanySerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = CompanyFilter
    
    @log_activity
    def user_company_profile(self, request,  *args, **kwargs):
        # employee_qs = EmployeeInformation.objects.filter(
        #     user__id = request.user.id
        # ).last()
        
        # if not employee_qs:
        #     return ResponseWrapper(error_msg='Employee Information is Not Found', error_code=404)
        
        # company_qs = employee_qs.employee_company
        company_qs = Company.objects.all().last()
        
        if not company_qs:
            return ResponseWrapper(error_msg=f"For Company Information is Not Found", error_code=404)
        
        serializer = CompanyDetailsSerializer(company_qs)
        return ResponseWrapper(msg="Success",data=serializer.data, status=200)
  
  
class TaxCategoryViewSet(CustomViewSet):
    queryset = TaxCategory.objects.all().order_by('name')
    lookup_field = 'slug'
    serializer_class = TaxCategorySerializer
    permission_classes = [CheckCustomPermission]
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.OrderingFilter,
    # )
    # filterset_class = CompanyFilter
    
class SMSMailSendLogViewSet(CustomViewSet):
    queryset = SMSMailSendLog.objects.all().order_by('username')
    lookup_field = 'id'
    serializer_class = SMSMailSendLogSerializer
    permission_classes = [CheckCustomPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SMSMailSendLogFilter
    
class UserNotificationViewSet(CustomViewSet):
    queryset = UserNotification.objects.all().order_by('created_at')
    lookup_field = 'id'
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = UserNotificationFilter
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @log_activity
    def list(self, request, *args, **kwargs):
        # qs = self.filter_queryset(self.get_queryset()).filter()
        qs = self.filter_queryset(self.get_queryset()).filter(user_information = request.user)
        serializer_class = self.get_serializer_class()

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
