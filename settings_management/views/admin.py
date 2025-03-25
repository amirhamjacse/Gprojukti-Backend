from django.db.models import Q
from base.filters import *
from human_resource_management.serializers.dashboard import DashboardPaymentAmountListSerializer, ShopWisePaymentCollectionListSerializer
from location.models import POSArea, POSRegion
from order.models import Order, OrderPaymentLog
from settings_management.filters import ShopDayEndFilter
from settings_management.filters import SliderFilter
from settings_management.models import *
from settings_management.serializers import *
from utils.actions import activity_log
from utils.base import get_user_store_list
from utils.calculate import show_wise_day_end_calculation
from utils.generates import unique_slug_generator
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from utils.decorators import log_activity
from utils.permissions import *
import re
from gporjukti_backend_v2.settings import TODAY
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime, timedelta


from django.utils import timezone

from utils.send_sms import otp_send_sms, send_email
class SliderViewSet(CustomViewSet):
    queryset = Slider.objects.all().order_by('name')
    lookup_field = 'pk'
    serializer_class = SliderSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SliderFilter 
    
    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            self.serializer_class = SliderCreateUpdateSerializer
        else:
            self.serializer_class = SliderSerializer

        return self.serializer_class

    @log_activity
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
            
            try:
                qs = serializer.save()
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()

            activity_log(qs, request,serializer)
            
            serializer = SliderSerializer(qs)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    
    # ..........***.......... Update ..........***..........
    @log_activity
    def update(self, request, slug, **kwargs):

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        if serializer.is_valid(): 
            qs = Slider.objects.filter(slug = slug).last()

            if not qs:
                return ResponseWrapper(error_code=406, error_msg='Not Found', 
                status=406)
            
            # ....NOTE...: Unique Slug Check :....START....

            qs = serializer.update(instance=qs, validated_data=serializer.validated_data)

            if slug:
                qs.slug = slug
                qs.save()

            try:
                if qs:
                    qs.updated_by_id = self.request.user.id
                    qs.save()
            except:
                qs = qs

            serializer = self.serializer_class(instance=qs)

            # Save Logger for Tracking 
            activity_log(qs, request,serializer)
            
            
            serializer = SliderSerializer(qs)

            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
class ShopDayEndViewSet(CustomViewSet):
    # queryset = ShopDayEnd.objects.all().order_by('-day_end_date')
    queryset = ShopDayEnd.objects.all().order_by('-day_end_date__date').distinct('day_end_date__date', 'shop__name')
    lookup_field = 'pk'
    serializer_class = ShopDayEndSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ShopDayEndFilter 
    
    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            self.serializer_class = ShopDayEndCreateSerializer
        elif self.action in ["update"]:
            self.serializer_class = ShopDayEndCreateSerializer
        else:
            self.serializer_class = ShopDayEndSerializer

        return self.serializer_class
    
    
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
        # ..........***.......... Get All Data ..........***..........
    @log_activity
    def list(self, request, *args, **kwargs): 
        store_qs = get_user_store_list(request_user=request.user)  
        
        qs = self.filter_queryset(self.get_queryset()).filter(shop__slug__in=store_qs.values_list('slug', flat=True))
        
        serializer_class = self.get_serializer_class()
        print(f"tttt, {qs.count()}")

        page_qs = self.paginate_queryset(qs)
        serializer = serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
    
    @log_activity
    def not_shop_day_end_create(self, request, *args, **kwargs): 
        
        shop_list_qs = OfficeLocation.objects.filter(office_type = "STORE", is_active = True).exclude(name__icontains = "Test")
        
        yesterday = timezone.now().date() - timedelta(days=1)
        
        for shop in shop_list_qs:
            day_end_qs = ShopDayEnd.objects.filter(
                shop__slug = shop.slug, 
                day_end_date__date = yesterday
            ).exclude(shop__name__icontains = "Agargaon").last()
            
            # print(f'Last Name = {shop.name}')
            user_qs = UserAccount.objects.filter(last_name__icontains = shop.name).last()
            
            if not day_end_qs and (shop.name != "GProjukti.com - Agargaon"):
                 
                shop_day_end =  show_wise_day_end_calculation(shop_qs = shop,
                                                              request_user = user_qs)
                print(f"Shop Name = {shop.name}")
            
        
        return ResponseWrapper(msg="Success", status=200)

    @log_activity
    def today_shop_sell_details(self, request, *args, **kwargs):
        shop_qs = get_user_store_list(request_user=request.user).last()
        
        context =  show_wise_day_end_calculation(shop_qs = shop_qs, request_user = request.user)
            
        return ResponseWrapper(data=context, msg='created', status=200)
    
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        shop_slug = request.data.get('shop_slug')
        
        if not shop_slug:
            return ResponseWrapper(error_msg='Shop Slug is required', error_code=400)
        
        
        # shop_qs = OfficeLocation.objects.filter(slug = shop_slug).last()
        
        shop_qs = OfficeLocation.objects.filter(slug = shop_slug, office_type = 'STORE').last()
        
        if not shop_qs:
            return ResponseWrapper(error_msg="Shop Information is Not Found", error_code=404) 
        
        today = timezone.now().date()
        
        shop_day_end_qs = ShopDayEnd.objects.filter(
            shop = shop_qs, day_end_date__date = today
        ).last()
        
        if shop_day_end_qs:
            return ResponseWrapper(error_msg=f"'{shop_qs.name}',You Already Done, Your 'Shop Day End', Thank You", error_code=404) 
        try:
            if serializer.is_valid():
                if shop_slug:
                    slug = unique_slug_generator(name = shop_slug) 
                    
                serializer.validated_data['created_by'] = request.user
                try:
                    serializer.validated_data['slug'] = slug
                except:
                    pass
                
                serializer.validated_data.pop('shop_slug')
                serializer.validated_data['shop'] = shop_qs 
                
                # today = today - timedelta(days=1) - timedelta(hours=6)
                
                try:
                    qs = serializer.save()
                    if slug:
                        qs.slug = slug
                        qs.day_end_date = today
                        qs.save()
                        
                except:
                    qs = serializer.save()

                serializer = ShopDayEndSerializer(qs)
                
                
                qs = ShopDayEnd.objects.filter(
                    shop = shop_qs, day_end_date__date = today
                ).last()
                    
                total_sell_amount = 0
                total_mfs_amount = 0
                
                if qs:
                    total_sell_amount = (qs.retail_sell_amount + qs.e_retail_sell_amount + qs.ecommerce_collection_amount)
                    
                    day_end_date = qs.day_end_date + timedelta(hours=6)
                    
                    day_end_date_plus_six_hours = day_end_date.strftime('%B %d, %Y at %I:%M %p')
                
                
                    day_end_message = (
                        f"Date: {day_end_date_plus_six_hours},\n"
                        f"Branch: {qs.shop.name},\n"
                        f"Total Collection: {total_sell_amount},\n"
                        f"Retail Sale Amount: {qs.retail_sell_amount},\n"
                        f"Total GSheba Sale Amount: {qs.retail_gsheba_sell_amount},\n"
                        f"Ecommerce Collection: {qs.ecommerce_collection_amount},\n"
                        f"Corporate Sell: {qs.corporate_sell_amount},\n"
                        f"Warranty Claim Qty: {qs.warranty_claim_quantity},\n"
                        f"Total GSheba Claim Qty: {qs.gsheba_claim_quantity},\n"
                        f"Total Refund Amount: {qs.refund_amount},\n"
                        f"Total MFS Amount: {total_mfs_amount},\n"
                        f"Total B2B Amount: {qs.total_b2b_sell_amount},\n"
                        f"Total Bank Deposit: {qs.total_bank_deposit_amount},\n"
                        f"Total Expenses: {qs.total_expense_amount}"
                    )

                    subject = f"G-Projukti.com Day-End at {qs.day_end_date.date()}"
                    
                    print(f"Day End Message = {day_end_message}")
                    
                    all_phone_number_list = []
                    
                    shop_phone_number = shop_qs.primary_phone
                    pos_area_phone_number = None
                    pos_region_phone_number = None
                    
                    all_phone_number_list.append(shop_phone_number)

                    pos_area_qs = POSArea.objects.filter(name=shop_qs.pos_area_name).last()
                    if pos_area_qs and pos_area_qs.phone:
                        pos_area_phone_number = pos_area_qs.phone
                        all_phone_number_list.append(pos_area_phone_number)
                                        
                    pos_region_qs = POSRegion.objects.filter(name=shop_qs.pos_region_name).last()
                    if pos_region_qs and pos_region_qs.phone:
                        pos_region_phone_number = pos_region_qs.phone
                        all_phone_number_list.append(pos_region_phone_number)
                                
                    addition_numbers = ['01819244200', '01755543184', '0701221277']
                    
                    # addition_numbers = ["01865650850"]

                    all_phone_number_list.extend(addition_numbers)
                    
                    print(f"All Phone Number = {all_phone_number_list}")
                    
                    for username in addition_numbers:
                    # for username in all_phone_number_list:
                        try:
                            otp_send_sms(phone=username, subject=subject, body=day_end_message)
                        except:
                            pass
                        
                        print(f"Phone Number = {username}")
                
            
                return ResponseWrapper(data=serializer.data, msg='created', status=200)
        except:
            return ResponseWrapper(msg='created', status=200)
        
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    
    # # ..........***.......... Update ..........***..........

    # def update(self, request, slug, **kwargs):

    #     serializer_class = self.get_serializer_class()
    #     serializer = serializer_class(data=request.data, partial=True)

    #     if serializer.is_valid(): 
    #         qs = Slider.objects.filter(slug = slug).last()

    #         if not qs:
    #             return ResponseWrapper(error_code=406, error_msg='Not Found', 
    #             status=406)
            
    #         # ....NOTE...: Unique Slug Check :....START....

    #         qs = serializer.update(instance=qs, validated_data=serializer.validated_data)

    #         if slug:
    #             qs.slug = slug
    #             qs.save()

    #         try:
    #             if qs:
    #                 qs.updated_by_id = self.request.user.id
    #                 qs.save()
    #         except:
    #             qs = qs

    #         serializer = self.serializer_class(instance=qs)

    #         # Save Logger for Tracking 
    #         activity_log(qs, request,serializer)
            
            
    #         serializer = SliderSerializer(qs)

    #         return ResponseWrapper(data=serializer.data)
    #     else:
    #         return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    
    @log_activity
    def day_end_message_and_mail(self, request, *args, **kwargs):
        today = settings.TODAY.date()
        
        day_end_qs = ShopDayEnd.objects.filter(day_end_date__date=today, shop__office_type = "STORE", shop__is_shown_in_website = True)
        
        day_end_message = []
        
        for day_end in day_end_qs:
            print('Processing day end for shop:', day_end.shop.name)
            
            user_information_qs = UserInformation.objects.filter(user=day_end.created_by)
            
            shop_qs = day_end.shop
            
            day_end_details = show_wise_day_end_calculation(shop_qs=shop_qs, request_user=day_end.created_by)
            
            total_sell_amount = day_end_details['retail_sell_amount'] + day_end_details['total_retail_gsheba_amount'] + \
                                day_end_details['total_e_retail_sell_amount'] + day_end_details['total_ecommerce_collection'] + \
                                day_end_details['total_corporate_collection'] + day_end_details['total_b2b_collection']
            
            total_mfs_amount = sum(payment['total_amount'] for payment in day_end_details['payment_collection_amount'])
            
            day_end_date = day_end.day_end_date
            day_end_date_plus_six_hours = day_end_date + timedelta(hours=6)
            
            print('Day end details:', day_end_details)
            
            html_message = f'''<html>
                <p>
                    <strong>Date:</strong> {day_end_date_plus_six_hours.strftime('%B %d, %Y at %I:%M %p')},<br>
                    <strong>Branch:</strong> {day_end_details['shop_name']},<br>
                    <strong>Total Collection:</strong> {total_sell_amount},<br>
                    <strong>Retail Sale Amount:</strong> {day_end_details['retail_sell_amount']},<br>
                    <strong>Total GSheba Sale Amount:</strong> {day_end_details['total_retail_gsheba_amount']},<br>
                    <strong>E-Retail Collection:</strong> {day_end_details['total_e_retail_sell_amount']},<br>
                    <strong>Ecommerce Collection:</strong> {day_end_details['total_ecommerce_collection']},<br>
                    <strong>Corporate Sell:</strong> {day_end_details['total_corporate_collection']},<br>
                    <strong>Warranty Claim Qty:</strong> {day_end_details['total_warranty_claim_quantity']},<br>
                    <strong>Total GSheba Claim Qty:</strong> {day_end_details['total_gsheba_claim_quantity']},<br>
                    <strong>Total Refund Amount:</strong> {day_end_details['total_refund_amount']},<br>
                    <strong>Total MFS Amount:</strong> {total_mfs_amount},<br>
                    <strong>Total B2B Amount:</strong> {day_end_details['total_b2b_collection']},<br>
                    <strong>Total Bank Deposit:</strong> {day_end.total_bank_deposit_amount},<br>
                    <strong>Total Expenses:</strong> {day_end.total_expense_amount}
                </p>
                <p>Thank you,<br>
                G-Projukti.com
                </p>
            </html>'''
            
            day_end_message.append(html_message)
            print(f"Processed day end for shop: {day_end.shop.name}")
        
        subject = f"G-Projukti.com Day-End For {today}"
        
        username = "01865650850"
        
        # otp_send_sms(phone=username, subject=subject, body=html_message)
        email_list = ["setusakilanasrin@gmail.com", "mayeenchy@kbg.com.bd", "rubyachy@kbg.com.bd", "gr.audit@kbg.com.bd", "setusakilanasrin@gmail.com", "razib.shams@kbg.com.bd"]
        
        # email_list = ["setusakilanasrin@gmail.com", "razib.shams@kbg.com.bd"]
        
        for email in email_list:
        
            send_email(email=email, subject=subject, body=day_end_message)
        
        # Optionally, send to other recipients
        # send_email(email="sazzad.reza@gprojukti.com", subject=subject, body=html_message)
        # send_email(email="gr.audit@kbg.com.bd", subject=subject, body=html_message)
        
        return ResponseWrapper(msg="Success", status=200)



class ShopDayEndMessageViewSet(CustomViewSet):
    queryset = ShopDayEndMessage.objects.all().order_by('-created_at')
    lookup_field = 'pk'
    serializer_class = ShopDayEndMessageSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [CheckCustomPermission]
    
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.OrderingFilter,
    # )
    # filterset_class = ShopDayEndFilter 
    
    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            self.serializer_class = ShopDayEndMessageCreateUpdateSerializer
        else:
            self.serializer_class = ShopDayEndMessageSerializer

        return self.serializer_class


class ShopPanelViewSet(CustomViewSet):
    queryset = ShopPanel.objects.all().order_by('name')
    lookup_field = 'slug'
    serializer_class = ShopPanelSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    
    # filterset_class = SliderFilter 
    
    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            self.serializer_class = ShopPanelSerializer
        elif self.action in ['list']:
            self.serializer_class = ShopPanelListSerializer
        else:
            self.serializer_class = ShopPanelDetailsSerializer

        return self.serializer_class


class ShopPanelHookViewSet(CustomViewSet):
    queryset = ShopPanelHook.objects.all().order_by('name')
    lookup_field = 'slug'
    serializer_class = ShopPanelHookSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    
    # filterset_class = SliderFilter 
    
    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            self.serializer_class = ShopPanelHookCreateUpdateSerializer
        else:
            self.serializer_class = ShopPanelHookSerializer

        return self.serializer_class
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        name = ''
        
        if request.data.get('name'):
            name = request.data.get('name')
        else:
            name = name
            
        qs = self.queryset.filter(name = request.data.get('name'))
        
            
        shop_panel_slug = request.data.pop('shop_panel_slug')
        product_list = request.data.pop('product_list')
        
        if serializer.is_valid():
            if name:
                slug = unique_slug_generator(name = name) 
                
            shop_panel = shop_panel_slug
            
            shop_panel_qs = ShopPanel.objects.filter(
                slug = shop_panel
            ).last()
            
            if not shop_panel_qs:
                return ResponseWrapper(error_msg= "Shop Hook is Not Found", status=400, error_code=404)
                
            serializer.validated_data['created_by'] = request.user
            serializer.validated_data['shop_panel'] = shop_panel_qs
            
            
            try:
                serializer.validated_data['slug'] = slug
            except:
                pass
            
            try:
                qs = serializer.save()
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()
                
                
            for item in product_list:
                product_slug = item.get('product_slug')
                serial_no = item.get('serial_no')
                remarks = item.get('remarks')
                is_active = item.get('is_active')
                
                product_qs = Product.objects.filter(slug = product_slug).last()
                if not product_qs:
                    return ResponseWrapper(error_msg= "Product Is Not Found", status=400, error_code=400)
                
                hook_product_qs = HookProduct.objects.create(
                    product = product_qs,
                    shop_panel_hook = qs,
                    serial_no = serial_no,
                    remarks = remarks,
                    is_active = is_active,
                    created_by = request.user,
                )

            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    
    @log_activity
    def update(self, request,slug, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        
        qs = ShopPanelHook.objects.filter(slug=slug)
        hook_qs = ShopPanelHook.objects.filter(slug=slug).last()
        if not qs:
            return ResponseWrapper(error_code=406, error_msg='Not Found', 
            status=406)
                   
        # qs = self.queryset.filter(name = request.data.get('name'))
        
            
        # shop_panel_slug = request.data.pop('shop_panel_slug')
        product_list = request.data.pop('product_list')
        
        if serializer.is_valid():
            
            shop_panel = qs.last().shop_panel.slug
            
            shop_panel_qs = ShopPanel.objects.filter(
                slug = shop_panel
            ).last()
            
            if not shop_panel_qs:
                return ResponseWrapper(error_msg= "Shop Hook is Not Found", status=400, error_code=404)
                
            # serializer.validated_data['created_by'] = request.user
            serializer.validated_data['shop_panel'] = shop_panel_qs
            
            
            # qs = serializer.update(instance=qs, validated_data=serializer.validated_data)
            
            qs = qs.update(
                name = qs.last().name
            )

            for item in product_list:
                product_slug = item.get('product_slug')
                serial_no = item.get('serial_no')
                remarks = item.get('remarks')
                is_active = item.get('is_active')
                
                product_qs = Product.objects.filter(slug = product_slug).last()
                if not product_qs:
                    return ResponseWrapper(error_msg= "Product Is Not Found", status=400, error_code=400)
                
                hook_product_qs = HookProduct.objects.create(
                    product = product_qs,
                    shop_panel_hook = hook_qs,
                    serial_no = serial_no,
                    remarks = remarks,
                    is_active = is_active,
                    created_by = request.user,
                )

            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)

class HookProductViewSet(CustomViewSet):
    queryset = HookProduct.objects.all().order_by('serial_no')
    lookup_field = 'slug'
    serializer_class = HookProductSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    
    # filterset_class = SliderFilter 
    
    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            self.serializer_class = HookProductCreateUpdateSerializer
        else:
            self.serializer_class = HookProductSerializer

        return self.serializer_class
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
        product_slug = ''
        
        product_slug = request.data.get('product_slug')
        shop_panel_hook_slug = request.data.get('shop_panel_hook_slug')
        
        if not product_slug:
            return ResponseWrapper(error_msg= "Product Is Mandatory", status=400, error_code=400)
        
        if not shop_panel_hook_slug:
            return ResponseWrapper(error_msg= "Shop Hook Is Mandatory", status=400, error_code=400)
        
        product_qs = Product.objects.filter(slug = product_slug).last()
        shop_panel_hook_qs = ShopPanelHook.objects.filter(slug = shop_panel_hook_slug).last()
        
        if not product_qs:
            return ResponseWrapper(error_msg= "Product Is Not Found", status=400, error_code=400)
        
        if not shop_panel_hook_qs:
            return ResponseWrapper(error_msg= "Shop Hook Is Not Found", status=400, error_code=400)
        
        shop_panel_hook_slug = request.data.pop('shop_panel_hook_slug')
        product_slug = request.data.pop('product_slug')
        
        name = shop_panel_hook_qs.name
        
        if serializer.is_valid():
            if name:
                slug = unique_slug_generator(name = name) 
                  
            serializer.validated_data['created_by'] = request.user
            serializer.validated_data['shop_panel_hook'] = shop_panel_hook_qs
            serializer.validated_data['product'] = product_qs
            
            try:
                serializer.validated_data['slug'] = slug
            except:
                pass
            
            try:
                qs = serializer.save()
                if slug:
                    qs.slug = slug
                    qs.save()
                    
            except:
                qs = serializer.save()

            activity_log(qs, request,serializer)

            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)