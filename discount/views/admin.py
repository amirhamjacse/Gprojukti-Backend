from discount.models import *
from discount.serializers import *
from human_resource_management.models.employee import EmployeeInformation
from product_management.models.category import Category
from product_management.models.product import *
from user.models import UserType
from utils.actions import activity_log
from utils.calculate import calculate_promo_code
from utils.custom_veinlet import CustomViewSet
from utils.generates import unique_slug_generator
from utils.permissions import CheckCustomPermission
from utils.response_wrapper import ResponseWrapper
from utils.upload_image import image_upload
from django.utils import timezone
from discount.filters import *
from utils.decorators import log_activity

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated

class DiscountViewSet(CustomViewSet):
    queryset = Discount.objects.all()
    lookup_field = 'pk'
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = DiscountFilter
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            self.serializer_class = DiscountSerializer
        elif self.action in ['list']:
            self.serializer_class = DiscountListSerializer
        elif self.action in ['discount_add_in_product_or_category']:
            self.serializer_class = productWiseDiscountPromoCodeAddSerializer
        else:
            self.serializer_class = DiscountDetailsSerializer

        return self.serializer_class

    @log_activity
    def discount_overview_list(self, request, *args, **kwargs):
        
        employee_qs = EmployeeInformation.objects.all().filter(employee_id__icontains = "GPRO-")
        
        type_qs = UserType.objects.filter(name__icontains = "Shop").last()
        
        for i in employee_qs:
            user_information_qs = UserInformation.objects.filter(
                user__email = i.user.email
            ).last()
            
            print(f"user_information_qs = {user_information_qs.name} {user_information_qs.user_type.name}")
            
            user_information_qs.user_type = type_qs
            user_information_qs.save()
            
            print(f"After user_information_qs = {user_information_qs.name} {user_information_qs.user_type.name}")
            
            user_qs = UserAccount.objects.filter(
                email = i.user.email
            ).last()
            
            # user_qs.groups
            
        
        context = [
            {
                'msg': "Total Active Discount",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Active Deal of the week",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Active Campaigns",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Upcoming Discount",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    # ..........***.......... Create ..........***..........
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        name = ''
        
        if request.data.get('name'):
            name = request.data.get('name')
            
        qs = self.queryset.filter(name = request.data.get('name'))
        
        if qs:
            return ResponseWrapper(error_msg="Name is Already Found", error_code=400)
      
        if serializer.is_valid():
            if name:
                slug = unique_slug_generator(name = name) 
                
            serializer.validated_data['created_by'] = request.user
            try:
                serializer.validated_data['slug'] = slug
            except:
                pass
            
            image_file = serializer.validated_data.pop('image', None)
            
            path = 'discount'
            
            if image_file:
                image = image_upload(file=image_file, path=path)
                serializer.validated_data['image'] = image
            
            employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            if not employee_qs or not employee_qs.employee_company:
                return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
            company_id = employee_qs.employee_company
            
            serializer.validated_data['company'] = company_id
            
            schedule_type = request.data.get('schedule_type')
            today = timezone.now()
            
            
            if schedule_type=='DATE_WISE':
                start_date = request.data.get('start_date')
                end_date = request.data.get('end_date')
                if not start_date or not end_date:
                    return ResponseWrapper(error_msg='Date Range is Required', error_code=400)
                
            else:
                start_time = request.data.get('start_time')
                end_time = request.data.get('end_time')
                if not start_time and not end_time:
                    return ResponseWrapper(error_msg='Time Range is Required', error_code=400)
                
            try:
                qs = serializer.save(
                    image = image
                )
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()

            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


    def update(self, request, slug, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        qs = self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_code=406, error_msg='Slug is Already Exist', status=406)
        
        existing_promo_code_qs = self.queryset.filter(slug = slug).exclude(slug = slug)
        
        if existing_promo_code_qs:
            return ResponseWrapper(error_code=406, error_msg='Slug is Already Exist', status=406)

        if serializer.is_valid():
            image_file = serializer.validated_data.pop('image', None)
            
            path = 'discount'
            
            if image_file:
                image = image_upload(file=image_file, path=path)
                serializer.validated_data['image'] = image
            
            # employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            # if not employee_qs or not employee_qs.employee_company:
            #     return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400, status = 400)
            
            # company_id = employee_qs.employee_company
            company_id = Company.objects.all().last()
            
            serializer.validated_data['company'] = company_id
            
            qs = serializer.update(instance=qs, validated_data=serializer.validated_data)
            
            try:
                if qs:
                    qs.updated_by_id = self.request.user.id
                    qs.save()
            except:
                qs = qs

            serializer = self.serializer_class(instance=qs)

            # Save Logger for Tracking 
            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400, status = 400)
        
    @log_activity
    def discount_add_in_product_or_category(self, request, slug, **kwargs):
        discount_qs = Discount.objects.filter(slug = slug).last()
        if not discount_qs:
            return ResponseWrapper(error_msg="Discount is Not Found", error_code=404, status = 404)
        
        category_list = request.data.get('category')
        product_list = request.data.get('product')
        
        if category_list:
            for category in category_list:
                slug = category.get('slug')
                category_qs = Category.objects.filter(slug = slug).last()
                if not category_qs:
                    return ResponseWrapper(error_msg=f"{slug} is Not Found", error_code=404)
                
                category_qs.discount = discount_qs
                category_qs.save()
                
                product_price_qs = ProductPriceInfo.objects.filter(product__category__slug = slug)
                
                product_price_qs.update(discount = discount_qs)
        
        
        if product_list:
            for product in product_list: 
                slug = product.get('slug')
                product_price_qs = ProductPriceInfo.objects.filter(product__slug = slug)
                if not product_price_qs:
                    return ResponseWrapper(error_msg=f"{slug} is Not Found", error_code=404)
                
                product_price_qs.update(discount = discount_qs)
        
        return ResponseWrapper(msg = "Success", status= 200)
 

class PromoCodeViewSet(CustomViewSet):
    queryset = PromoCode.objects.all()
    lookup_field = 'pk'
    serializer_class = PromoCodeListSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = PromoCodeFilter
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = PromoCodeSerializer
        elif self.action in ['update']:
            self.serializer_class = PromoCodeUpdateSerializer
        elif self.action in ['list']:
            self.serializer_class = PromoCodeListSerializer
        elif self.action in ['check_promo_code']:
            self.serializer_class = CheckPromoCodeSerializer
        elif self.action in ['promo_code_add_in_product_or_category']:
            self.serializer_class = productWiseDiscountPromoCodeAddSerializer
        else:
            self.serializer_class = PromoCodeDetailsSerializer

        return self.serializer_class
    
    
    @log_activity
    def promo_code_overview_list(self, request, *args, **kwargs):
        context = [
            {
                'msg': "Total Active Promo Code",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Upcoming Promo Code",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Online Promo Code",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            },
            {
                'msg': "Total Offline Promo Code",
                'quantity': random.randint(333, 7342),
                'ratio': f"{random.randint(21, 99)}%",
            }
        ]
        return ResponseWrapper(data= context, msg="Success", status=200)
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        promo_code = ''
        
        if request.data.get('promo_code'):
            promo_code = request.data.get('promo_code')
            
        qs = self.queryset.filter(promo_code = request.data.get('promo_code'))
        
        if qs:
            return ResponseWrapper(error_msg="Promo Code is Already Found", error_code=400)
      
        if serializer.is_valid():
            if promo_code:
                slug = unique_slug_generator(name = promo_code) 
                
            serializer.validated_data['created_by'] = request.user
            try:
                serializer.validated_data['slug'] = slug
            except:
                pass
            
            image_file = serializer.validated_data.pop('image', None)
            
            path = 'promo_code'
            
            if image_file:
                image = image_upload(file=image_file, path=path)
                serializer.validated_data['image'] = image
            
            # employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            # if not employee_qs or not employee_qs.employee_company:
            #     return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
            company_id = Company.objects.all().last()
            
            # company_id = employee_qs.employee_company
            
            serializer.validated_data['company'] = company_id
            
            schedule_type = request.data.get('schedule_type')
            today = timezone.now()
            
            
            if schedule_type=='DATE_WISE':
                start_date = request.data.get('start_date')
                end_date = request.data.get('end_date')
                if not start_date or not end_date:
                    return ResponseWrapper(error_msg='Date Range is Required', error_code=400)
                
            else:
                start_time = request.data.get('start_time')
                end_time = request.data.get('end_time')
                if not start_time and not end_time:
                    return ResponseWrapper(error_msg='Time Range is Required', error_code=400)
                
            try:
                qs = serializer.save(
                    image = image
                )
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()

            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    @log_activity
    def update(self, request, slug, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        
        qs = self.queryset.filter(slug = slug).last()
        
        if not qs:
            return ResponseWrapper(error_code=406, error_msg='Slug is Already Exist', status=406)
        
        existing_promo_code_qs = self.queryset.filter(slug = slug).exclude(slug = slug)
        
        if existing_promo_code_qs:
            return ResponseWrapper(error_code=406, error_msg='Slug is Already Exist', status=406)

        if serializer.is_valid():
            image_file = serializer.validated_data.pop('image', None)
            
            path = 'promo_code'
            
            if image_file:
                image = image_upload(file=image_file, path=path)
                serializer.validated_data['image'] = image
            
            
            employee_qs = EmployeeInformation.objects.filter(user=request.user).last()
            if not employee_qs or not employee_qs.employee_company:
                return ResponseWrapper(error_msg='You Have Not Enough Permission', error_code=400)
            
            company_id = employee_qs.employee_company
            
            serializer.validated_data['company'] = company_id
            
            qs = serializer.update(instance=qs, validated_data=serializer.validated_data)
            
            try:
                if qs:
                    qs.updated_by_id = self.request.user.id
                    qs.save()
            except:
                qs = qs

            serializer = PromoCodeListSerializer(instance=qs)

            # Save Logger for Tracking 
            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)


    @log_activity
    def check_promo_code(self, request, *args, **kwargs):
        promo_code = request.data.get('promo_code')
        order_type = request.data.get('order_type')
        product_list = request.data.get('product_list')
        
        promo_code_qs = PromoCode.objects.filter(promo_code = promo_code, promo_type = order_type).last()
        
        if not promo_code_qs:
            return ResponseWrapper(error_msg=f"'{promo_code}', Promo Code is Not Valid", status=404)
        
        if not product_list:
            return ResponseWrapper(error_msg=f"Product is not Add in Your Cart", status=404)
        
        promo_code_price_info_details  = calculate_promo_code(promo_code = promo_code, order_type = order_type, product_list = product_list)
        
        price_info_details = promo_code_price_info_details.get('price_info_details')
        
        error_msg_list = promo_code_price_info_details.get('error_msg_list')
        
        total_promo_discount_amount = promo_code_price_info_details['price_info_details'].get('total_promo_discount_amount')
        
        # if total_promo_discount_amount < 1:
        #     return ResponseWrapper(error_msg=f"Promo Code is Not Valid for Your Product", status=404)
        
        # error_msg_list = context('error_msg_list')
        
        if error_msg_list:
            return ResponseWrapper(data=price_info_details, error_msg=str(error_msg_list), status=200)
                                   
        return ResponseWrapper(data=price_info_details, msg='Applied Successfully', status=200)

    @log_activity
    def promo_code_add_in_product_or_category(self, request, slug, **kwargs):
        qs = PromoCode.objects.filter(slug = slug).last()
        if not qs:
            return ResponseWrapper(error_msg="Discount is Not Found", error_code=404)
        
        category_list = request.data.get('category')
        product_list = request.data.get('product')
        
        if category_list:
            for category in category_list:
                slug = category.get('slug')
                category_qs = Category.objects.filter(slug = slug).last()
                if not category_qs:
                    return ResponseWrapper(error_msg=f"{slug} is Not Found", error_code=404)
                
                product_price_qs = ProductPriceInfo.objects.filter(product__category__slug = slug)
                
                product_price_qs.update(promo_code = qs)
        
        
        if product_list:
            for product in product_list: 
                slug = product.get('slug')
                product_price_qs = ProductPriceInfo.objects.filter(product__category__slug = slug)
                if not product_price_qs:
                    return ResponseWrapper(error_msg=f"{slug} is Not Found", error_code=404)
                
                product_price_qs.update(promo_code = qs)
        
        return ResponseWrapper(msg = "Success", status= 200)
