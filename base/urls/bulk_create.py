from django.urls import path
from base.views.bulk_create import *

urlpatterns = [
     path('bulk_command/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_command'},  name='bulk_command')),
     
     path('bulk_payment_type_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_payment_type_create'},  name='bulk_payment_type_create')),
     
     path('bulk_employee_information_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_employee_information_create'},  name='bulk_employee_information_create')),
     
     path('bulk_pre_data_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_pre_data_create'},  name='bulk_pre_data_create')),
     
     path('bulk_slider_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_slider_create'},  name='bulk_slider_create')),
     
     path('bulk_product_stock_create_for_warehouse/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_product_stock_create_for_warehouse'},  name='bulk_product_stock_create_for_warehouse')),
     
     path('bulk_delivery_method_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_delivery_method_create'},  name='bulk_delivery_method_create')),
     
     path('bulk_pos_area_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_pos_area_create'},  name='bulk_pos_area_create')),
     
     path('bulk_pos_region_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_pos_region_create'},  name='bulk_pos_region_create')),
     
     path('bulk_user_create/',
          BulkDataUploadViewSet.as_view({'post': 'user_create'},  name='bulk_user_create')),
     
     path('bulk_division_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_division_create'},  name='bulk_division_create')),
     
     path('bulk_district_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_district_create'},  name='bulk_district_create')),
     
     path('bulk_area_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_area_create'},  name='bulk_area_create')),
     
     path('bulk_office_location_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_office_location_create'},  name='bulk_office_location_create')),
     
     path('bulk_category_group_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_category_group_create'},  name='bulk_category_group_create')),
     
     path('bulk_category_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_category_create'},  name='bulk_category_create')),
     
     path('bulk_sub_category_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_sub_category_create'},  name='bulk_sub_category_create')),
     
     path('bulk_brand_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_brand_create'},  name='bulk_brand_create')),
     
     path('bulk_supplier_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_supplier_create'},  name='bulk_supplier_create')),
     
     path('bulk_seller_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_seller_create'},  name='bulk_seller_create')),
     
     path('bulk_tax_category_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_tax_category_create'},  name='bulk_tax_category_create')), 
     
     path('bulk_product_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_product_create'},  name='bulk_product_create')),
     
     path('bulk_product_stock_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_product_stock_create'},  name='bulk_product_stock_create')),
     
     path('bulk_promo_code_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_promo_code_create'},  name='bulk_promo_code_create')),
     
     path('bulk_stock_transfer_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_stock_transfer_create'},  name='bulk_stock_transfer_create')),
     
     path('bulk_discount_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_discount_create'},  name='bulk_discount_create')),
     
     path('bulk_shop_day_end_create/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_shop_day_end_create'},  name='bulk_discount_create')),
     
     path('bulk_order_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_order_create'},  name='bulk_order_create')),
     
     path('bulk_shop_user_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_shop_user_create'},  name='bulk_shop_user_create')),
     
     path('bulk_ecommerce_order_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_ecommerce_order_create'},  name='bulk_ecommerce_order_create')),
     
     path('bulk_shop_sell_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_shop_sell_create'},  name='bulk_shop_sell_create')),
     
     path('bulk_stock_transfer_update/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_stock_transfer_update'},  name='bulk_stock_transfer_update')),
     
     path('bulk_barcode_status_update/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_barcode_status_update'},  name='bulk_barcode_status_update')),
     
     path('bulk_day_end_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_day_end_create'},  name='bulk_day_end_create')),
     
     path('bulk_barcode_update/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_barcode_update'},  name='bulk_barcode_update')),
     
     path('bulk_corporate_sell_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_corporate_sell_create'},  name='bulk_corporate_sell_create')),
     
     path('bulk_parental_product_create/',
          BulkDataUploadViewSet.as_view({'post': 'bulk_parental_product_create'},  name='bulk_parental_product_create')),
     
     path('multiple_user_permission_create/',
          BulkDataUploadViewSet.as_view({'get': 'multiple_user_permission_create'},  name='multiple_user_permission_create')),
     
     path('bulk_service_order_create/<invoice_no>/',
          BulkDataUploadViewSet.as_view({'get': 'bulk_service_order_create'},  name='bulk_service_order_create')),
]