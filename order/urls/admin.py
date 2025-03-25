from django.urls import path, include

from order.views.admin import *

urlpatterns = [
      path('order/',
            OrderViewSet.as_view({'post': 'create', 'get': 'list'},  name='order')),
      path('order_history_details_backup/',
            OrderViewSet.as_view({ 'get': 'order_history_details_backup'},  name='order_history_details_backup')),
      path('order_status_update/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_status_update'},  name='order_status_update')),
      path('order_remarks/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_remarks'},  name='order_remarks')),
      path('courier_service_add_in_order/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'courier_service_add_in_order'},  name='courier_service_add_in_order')),
      path('order_customer_info_address_update/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_customer_info_address_update'},  name='order_customer_info_address_update')),
      path('order_payment_log_update/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_payment_log_update'},  name='order_payment_log_update')),
      path('order_item_update/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_item_update'},  name='order_item_update')),
      path('order_item_remove/<order_item_id>/',
            OrderViewSet.as_view({'delete': 'order_item_remove'},  name='order_item_remove')),
      path('order_payment_log_remove/<slug>/',
            OrderViewSet.as_view({'delete': 'order_payment_log_remove'},  name='order_payment_log_remove')),
      path('order_item_status_log/<order_item_id>/',
            OrderViewSet.as_view({'get': 'order_item_status_log'},  name='order_item_status_log')),
      path('order_overview_list/<order_type>/',
            OrderViewSet.as_view({'get': 'order_overview_list'},  name='order_overview_list')),
      
      path('order_details/<invoice_no>/',
            OrderViewSet.as_view({'get': 'order_details'},  name='order_details')),
      path('pos_invoice_print/<invoice_no>/',
            OrderViewSet.as_view({'get': 'pos_invoice_print'},  name='pos_invoice_print')),
      path('delivery_method/',
            DeliveryMethodViewSet.as_view({'post': 'create', 'get': 'list'},  name='delivery_method')),
      
      path('order_invoice_print/<invoice_no>/',
            OrderViewSet.as_view({'get': 'order_invoice_print'},  name='order_invoice_print')),
      path('order_invoice_label_print/<invoice_no>/',
            OrderViewSet.as_view({'get': 'order_invoice_label_print'},  name='order_invoice_label_print')),
      path('return_pos_invoice_print/<invoice_no>/',
            OrderViewSet.as_view({'get': 'return_pos_invoice_print'},  name='return_pos_invoice_print')),
      
      path('multiple_order_invoice_print/',
            OrderViewSet.as_view({'post': 'multiple_order_invoice_print'},  name='multiple_order_invoice_print')),
      path('multiple_order_label_print/',
            OrderViewSet.as_view({'post': 'multiple_order_label_print'},  name='multiple_order_label_print')),
      path('order_list_download/',
            OrderDownloadViewSet.as_view({'get': 'list'},  name='order_list_download')),
      
      # Order Return 
      
      path('return_order_list/',
            OrderViewSet.as_view({'get': 'return_order_list'}, 
                                 name='return_order_list')),
      path('order_return_status_update/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_return_status_update'},
                                 name='order_return_status_update')),
      path('order_return_status_approved/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_return_status_approved_rejected'},
                                 name='order_return_status_approved')),
      path('order_return_status_rejected/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_return_status_approved_rejected'},
                                 name='order_return_status_rejected')),
      
      path('return_overview_list/',
            OrderViewSet.as_view({'get': 'return_overview_list'},  name='return_overview_list')),

      path('apply_promo_code/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'apply_promo_code'},  name='apply_promo_code')),
      # Order G-Sheba Return 
      
      path('gsheba_return_item_add/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'gsheba_return_item_add'},
                                 name='gsheba_return_item_add')),
      # Order Payment Refunded 
      
      path('order_refunded_payment_update/<invoice_no>/',
            OrderViewSet.as_view({'patch': 'order_refunded_payment_update'},
                                 name='order_refunded_payment_update')),
      # Service Order Status Change 
      
      path('service_order/',
            ServiceOrderViewSet.as_view({'post': 'create', 'get': 'list'},  name='service_order')),
      path('service_order/<invoice_no>/',
            ServiceOrderViewSet.as_view({'get': 'retrieve'},
                                 name='service_order')),
      path('service_order_status_update/<invoice_no>/',
            ServiceOrderViewSet.as_view({'patch': 'service_order_status_update'},
                                 name='service_order_status_update')),
      


    ]
  