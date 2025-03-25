from gporjukti_backend_v2 import settings
from gporjukti_backend_v2.settings import BASE_URL, TODAY
from order.models import *
from order.serializers import *
from human_resource_management.models.employee import EmployeeInformation
from product_management.models.product import ProductStock, Product
from product_management.utils import barcode_status_log
from user.models import UserType
from utils.actions import activity_log
from utils.calculate import generate_service_order_status_log, service_order_create_or_update, generate_order_status_log, offer_check, order_item_create, order_payment_log, sslcommerz_payment_create
from utils.custom_veinlet import CustomViewSet
from utils.generates import generate_invoice_no, generate_service_invoice_no, generate_transaction_number, unique_slug_generator
from utils.permissions import CheckCustomPermission
from utils.response_wrapper import ResponseWrapper
from utils.upload_image import image_upload
from utils.decorators import log_activity
from django.utils import timezone
from order.filters import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

from channels.layers import get_channel_layer

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from asgiref.sync import async_to_sync
from rest_framework.permissions import AllowAny, IsAuthenticated


class PublicOrderViewSet(CustomViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    lookup_field = 'pk'
    serializer_class = OrderListSerializer
    permission_classes = [CheckCustomPermission]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = OrderFilter
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = OrderCreateSerializer
        else:
            self.serializer_class = OrderListSerializer

        return self.serializer_class
    
    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @log_activity
    def create(self, request, *args, **kwargs):
        order_date = request.data.get('order_date')
        
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        area_slug = request.data.get('area_slug')
        address = request.data.get('address')
        address_type = request.data.get('address_type')
        delivery_method_slug = request.data.get('delivery_method_slug')
        order_type = request.data.get('order_type')
        payment_type = request.data.get('payment_type')
        payment_status = request.data.get('payment_status')
        promo_code = request.data.get('promo_code')
        employee_id = request.data.get('employee_id')
        total_advance_amount = request.data.get('total_advance_amount')
        shop = request.data.get('shop')
        pickup_shop = request.data.get('pickup_shop')
        
        order_item_list = request.data.get('order_item_list')
        order_payment_list = request.data.get('order_payment_list')
        
        print('sssssssssssssssssss', delivery_method_slug)
        delivery_method_qs = DeliveryMethod.objects.filter(slug=delivery_method_slug).last()
        
        if not delivery_method_qs:
            return ResponseWrapper(error_msg='Delivery Method is Not Found', status=404)
        
        if delivery_method_qs.delivery_type in ["SHOP_PICKUP", "STORE_SELL"] and not pickup_shop:
            return ResponseWrapper(error_msg='Pickup Shop ID is Mandatory', status=400)
        
        # Customer Information Create
        
        if '@' in phone:
            return ResponseWrapper(error_msg='Phone Number is Not Found', status=404)
        
        user_qs = UserAccount.objects.filter(
            Q( email =  email)
            | Q( phone =  phone)
            ).last()
        
        
        if not user_qs:
            user_qs = UserAccount.objects.create(
                first_name = first_name, last_name = last_name, 
                email = email, phone = phone, 
            )
        
        
        name = f"{first_name} {last_name}"
        
        user_information_qs = UserInformation.objects.filter(user__id = user_qs.id).last()
        
        if not user_information_qs:    
            user_info_slug = unique_slug_generator(name=name) if name else None
            
            if order_type == 'CORPORATE_SELL':
                user_type = 'Corporate'
                
            else:
                user_type = 'Customer'
                
            user_type_qs =  UserType.objects.filter(name = user_type).last()
            
            if not user_type_qs:
                user_type_qs = UserType.objects.create(name = user_type)
                
            user_information_qs = UserInformation.objects.create(
                name = name, slug = user_info_slug, 
                user_type = user_type_qs, created_by = request.user, user = user_qs
            )
            
        # Customer Address
        area_name = '-'
        district_name = '-'
        division_name = '-'
        country_name = '-'
        shop_qs = None
        pickup_shop_qs = None
        
        area_qs = Area.objects.filter(slug = area_slug).last()

        if not area_qs:
            return ResponseWrapper(error_msg='Area is Not Found', status=404)
        
        if area_qs:
            area_name = area_qs.name
            
            if area_qs.district:
                district_name = area_qs.district.name
                
            if area_qs.district.division:
                division_name = area_qs.district.division.name
                
            if area_qs.district.division.country:
                country_name = area_qs.district.division.country.name
        
        
        last_order_qs = Order.objects.all().order_by('-created_at').last()
        if last_order_qs:
            last_invoice_no = last_order_qs.invoice_no
        else:
            last_invoice_no = 'ONL000000001'
            
        invoice_no = generate_invoice_no(last_invoice_no)
        today = timezone.now()
        
        order_create_user = request.user
        
        if employee_id:
            employee_qs = EmployeeInformation.objects.filter(
                employee_id = employee_id
            ).last()
            if not employee_qs:
                return ResponseWrapper(error_msg='Employee Information is Not Found', status=404)
            
            order_create_user = employee_qs.user
            
        if order_type == 'PRE_ORDER' and not order_date:
            return ResponseWrapper(error_msg='Order Date is Mandatory', status=400)
            
        status = 'ORDER_RECEIVED'
        
        if order_type == 'POINT_OF_SELL':
            status = 'DELIVERED'
            
        if pickup_shop:
            pickup_shop_qs = OfficeLocation.objects.filter(slug = pickup_shop, office_type = "STORE").last()
            if not pickup_shop_qs:
                return ResponseWrapper(error_msg=f"{shop}, is Not Found", error_code=404)
        
        if shop:
            shop_qs = OfficeLocation.objects.filter(slug = shop, office_type = "STORE").last()
            if not shop_qs:
                return ResponseWrapper(error_msg=f"{shop}, is Not Found", error_code=404)
            
        if not shop and order_type in ['POINT_OF_SELL', "ON_THE_GO", "CORPORATE_SELL", "B2B_SELL"]:
            employee_qs = EmployeeInformation.objects.filter(user = request.user).last()
            if employee_qs:
                if not employee_qs.work_station:
                    return ResponseWrapper(error_msg=f"Shop Information is Not Found", error_code=404)
                shop_qs = employee_qs.work_station
            
        if not payment_status:
            payment_status = 'UNPAID'
            
        order_qs = Order.objects.create(
            invoice_no  = invoice_no,
            order_type = order_type,
            status = status,
            customer = user_information_qs,
            delivery_method = delivery_method_qs,
            payment_status = payment_status,
            payment_type = payment_type,
            area = area_qs,
            district_name = district_name,
            division_name = division_name,
            country_name = country_name,
            address = address,
            promo_code = promo_code,
            created_by = request.user
        )
        if not order_date:
            order_date = order_qs.created_at
            
        if order_qs and order_date:
            order_qs.order_date = order_date
            
        if order_qs.order_type == 'CORPORATE_SELL':
            order_qs.approved_status = 'INITIALIZED'
            
        if shop_qs:
            order_qs.shop = shop_qs
            
        if pickup_shop_qs:
            order_qs.pickup_shop = pickup_shop_qs
            
        order_qs.save()
        
        user_address_slug = unique_slug_generator(name=name) if name else None
        
        customer_address_log_qs = CustomerAddressInfoLog.objects.create(
            address_type = address_type, slug = user_address_slug,
            name = name, phone = phone, email = email,
            address = address, area_name = area_name, district_name=district_name,
            division_name = division_name, country_name = country_name,
            created_by = request.user, order = order_qs
        )
        
        for order_item in order_item_list:
            product_slug = order_item.get('product_slug')
            quantity = order_item.get('quantity')
            selling_price = order_item.get('selling_price') or 0.0 
            gsheba_amount = order_item.get('gsheba_amount') or 0.0
            barcode_number = order_item.get('barcode_number')
            
            created_by = request.user
            
            status_change_reason = 'Order Created By -'
            
            
            if order_type == 'POINT_OF_SELL':
                status = 'DELIVERED'
            else:
                status='ORDER_RECEIVED'
            
            order_item_qs = order_item_create(barcode_status =None,order_item_qs= None, order_qs = order_qs, product_slug = product_slug,quantity =  quantity, selling_price = selling_price, gsheba_amount = gsheba_amount, barcode_number = barcode_number, created_by = created_by, status_change_reason = status_change_reason, status=status )
            
            
            is_valid = order_item_qs.get('is_valid')
            error_msg = order_item_qs.get('error_msg')
            
            if not is_valid:
                return ResponseWrapper(error_msg=error_msg, status=404) 
            
            
        if order_payment_list:
            for order_payment in order_payment_list:
                transaction_no = order_payment.get('transaction_no')
                payment_method_slug = order_payment.get('payment_method_slug')
                received_amount = order_payment.get('received_amount')
                
                if payment_method_slug:
                    payment_qs =  PaymentType.objects.filter(
                        slug = payment_method_slug
                    ).last()
                    
                    if not payment_qs:
                        return ResponseWrapper(error_msg='Payment Method is Not Found', status=404)
                    
                payment_slug = unique_slug_generator(name=order_qs.invoice_no) if name else None
                
                request_user = request.user
                
                order_status = order_qs.status
                status='RECEIVED'
                
                
                order_payment_log(order_qs, payment_slug, payment_qs, order_status, received_amount, transaction_no, request_user, status)
                
        order_status_slug = unique_slug_generator(name=order_qs.invoice_no) if name else None
        
        serializer = OrderCreateSerializer(order_qs.id)
        
        profile_image_url = f"{BASE_URL}/assets/images/no-image-available.jpg"
        if user_information_qs.image:
            profile_image_url= user_information_qs.image
            
        status_change_by = {
                            'id': request.user.id,
                            'name': user_information_qs.name,
                            'email': request.user.email,
                            'profile_image_url': profile_image_url,
                            }
        
        order_status_log_qs =  OrderStatusLog.objects.create(
            slug = order_status_slug,
            order = order_qs, status = order_qs.status,
            status_display = 'Order Received',
            order_status_reason = f'Order Created By {name} at {order_qs.order_date}',
            order_status_change_at = today,
            status_change_by = status_change_by,
            created_by = request.user
        )
            

        # activity_log(qs = order_qs, request= request, serializer= serializer)
        
        calculate_order_price(order_qs)
        
        order_qs = Order.objects.filter(invoice_no = order_qs.invoice_no).last()
        
        order_payable_amount = 0.0
        
        if order_qs.total_advance_amount == 0.0:
            order_payable_amount = order_qs.total_payable_amount
        else:
            order_payable_amount = order_qs.total_advance_amount
        
        context = {
            'invoice_no': order_qs.invoice_no,
            'order_type': order_type,
            'order_date': order_qs.order_date,
            'total_advance_amount': order_payable_amount,
            'payment_status': order_qs.payment_status,
            'payment_type': order_qs.payment_type,
        }
        
        
        
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'admin-panel',
                {
                    'type': 'send_notification',
                    'data': f"An {order_qs.get_order_type_display()} Has Been Received"
                    # 'order': serializer.data
                }
            )
            logger.info(f'Notification sent for user {request.user.id} with order data: {serializer.data}')
            created_date_str = order_qs.created_at.strftime('%d %B, %Y at %I:%M %p')
        
            user_notification_qs = UserNotification.objects.create(
                title = f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()}",
                description=f"An {order_qs.get_order_type_display()} Has Been {order_qs.get_status_display()} By {request.user.email} at {created_date_str}",
                created_by = order_qs.updated_by, user_information= request.user
            )
        
            print('Success')
            
        except Exception as e:
            logger.error(f'Error sending notification: {e}')

        return ResponseWrapper(data=context, msg='created', status=200)

    @log_activity
    def order_details(self, request, invoice_no,  *args, **kwargs):
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', status=404)
        
        # if not (order_qs.customer.user == request.user):
        #     return ResponseWrapper(error_msg=f"You Have Not Enough Permission For '{invoice_no}' Order", status=400)
        
        serializer = OrderDetailsSerializer(instance=order_qs)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)
    
    @log_activity
    def list(self, request,  *args, **kwargs):
        order_qs = Order.objects.filter(customer__user = request.user)
        
        serializer = OrderListSerializer(instance=order_qs, many=True)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)

    @log_activity
    def ssl_order_payment(self, request,invoice_no,  *args, **kwargs):
        
        order_qs = Order.objects.filter(invoice_no = invoice_no).last()
        
        # order_qs = Order.objects.filter(invoice_no = invoice_no, customer__user = request.user).last()
        if not order_qs:
            return ResponseWrapper(error_msg='Order is Not Found', error_code=404)
        
        last_order_payment_qs = OrderPaymentLog.objects.all().last()

        if last_order_payment_qs.transaction_no:
            transaction_number = generate_transaction_number(last_transaction_no = last_order_payment_qs.transaction_no)
        else:
            transaction_number = generate_transaction_number(last_transaction_no = 'OSL00')
        
        order_payable_amount = 0.0
        if order_qs.total_advance_amount == 0.0:
            order_payable_amount = order_qs.total_payable_amount
            
        else:
            order_payable_amount = order_qs.total_advance_amount
            
        sslcommerz_data = {
            'ipn_url': f'{settings.SSL_BASE_URL}/api/v1.0/payment/customer/order/sslcommerz/ipn',
            'value_a': order_qs.id,
            'value_b': order_qs.customer_address_logs.last().name,
            'num_of_item': 2,
            'product_name': 'a,b',
            'store_name': 'gprojukti',
            'product_category': 'Deliverable',
            'product_profile': 'physical-goods',
            'store_name': 'gprojukti',
            'total_amount': order_payable_amount,
            'tran_id': transaction_number,
            'success_url': f'{settings.FRONTEND_BASE_URL}/checkout/success/{order_qs.invoice_no}',
            'fail_url': f'{settings.FRONTEND_BASE_URL}/checkout/fail/{order_qs.invoice_no}',
            'cancel_url': f'{settings.FRONTEND_BASE_URL}/checkout/cancel/{order_qs.invoice_no}',
        }
        response = sslcommerz_payment_create(data=sslcommerz_data, customer=request.user)
        
        print('REssssssssssssss', response)
        
        if not response:
            return ResponseWrapper(error_msg='Error response from SSlCommerz', error_code=417)
        
        print('REssssssssssssss', response)
        
        res_data = {
            'payment_gateway_url': response['GatewayPageURL'],
            'logo': response['storeLogo'],
            # 'store_name': response['store_name'],
        }
        
        
        print('fffffffffff', res_data)
        
        # try:
        #     # super(CustomerSSLCommerzOrderPaymentView, self).create(request, *args, **kwargs)
        #     # return Response(res_data, status=status.HTTP_201_CREATED)
        # except IntegrityError as err:
        #     return Response({'message': 'Error initializing SSLCommerz payment'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            slug = unique_slug_generator(name = invoice_no)
            
            # print(transaction_number, 'trx')
            
            order_payable_amount = 0.0
            
            if order_qs.total_advance_amount == 0.0:
                order_payable_amount = order_qs.total_payable_amount
                
            else:
                order_payable_amount = order_qs.total_advance_amount
            
            order_payment_qs = OrderPaymentLog.objects.create(
                transaction_no=transaction_number, slug = slug, order = order_qs,  remarks = str(response),
                created_by=request.user, received_amount = order_payable_amount
            )
        except:
            pass
        
        # serializer = OrderDetailsSerializer(instance=order_qs)
        
        # return ResponseWrapper(data=serializer.data, msg='Success', status=200)
        return ResponseWrapper(data=res_data, msg='Success', status=200)
