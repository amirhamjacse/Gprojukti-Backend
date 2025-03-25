from django.urls import path, include
from utils.upload_image import image_upload

from product_management.views.admin.product import *

urlpatterns = [
     path('product/',
          ProductViewSet.as_view({'post': 'create', 'get': 'list'},  name='product')),
     path('unique_product_code/',
          ProductViewSet.as_view({'get': 'unique_product_code'},  name='product')),
     path('product/<slug>/',
          ProductViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='product')),
     path('shop_product_list/',
          ProductViewSet.as_view({'get': 'shop_product_list'},  name='shop_product_list')),
     path('shop_product_list_barcode/',
          ProductViewSet.as_view({'get': 'shop_product_list_barcode'},  name='shop_product_list_barcode')),
     path('shop_product_list_pos/',
          ProductViewSet.as_view({'get': 'shop_product_list_pos'},  name='shop_product_list_pos')),

     # path('requisition_product_list/<shop_slug>/',
     #      ProductViewSet.as_view({'get': 'requisition_product_list'},  name='requisition_product_list')),
     path('product_overview_list/',
          ProductViewSet.as_view({'get': 'product_overview_list'},  name='product_overview_list')),
     path('shop_wise_product_list/',
          ProductViewSet.as_view({'get': 'shop_wise_product_list'},  name='shop_wise_product_list')),
     
     path('product_variant_create_update/<slug>/',
          ProductViewSet.as_view({'patch': 'product_variant_create_update'},  name='product_variant_create_update')),
     
     path('product_image_upload/',
          ProductViewSet.as_view({'patch': 'product_image_upload'},  name='product_image_upload')),
     path('product_variant_image_upload/<product_slug>/',
          ProductViewSet.as_view({'patch': 'product_variant_image_upload'},  name='product_variant_image_upload')),
     
     path('product_attribute/',
          ProductAttributeViewSet.as_view({'post': 'create', 'get': 'list'},  name='product_attribute')),
     path('product_attribute/<slug>/',
          ProductAttributeViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='product_attribute')),
     
     path('product_attribute_value/',
          ProductAttributeValueViewSet.as_view({'post': 'create', 'get': 'list'},  name='product_attribute_value')),
     path('product_attribute_value/<slug>/',
          ProductAttributeValueViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='product_attribute_value')),
     
     path('product_price_info_create/<product_slug>/',
          ProductViewSet.as_view({'post': 'product_price_info_create'},  name='product_price_info_create')),
     
     path('product_attribute_value_create_update/<product_slug>/',
          ProductViewSet.as_view({'patch': 'product_attribute_value_create_update'},  name='product_attribute_value_create_update')),

     path('product_description_create/<slug>/',
          ProductViewSet.as_view({'patch': 'product_description_create'},  name='product_description_create')),
     
     path('product_warranty_create/<slug>/',
          ProductViewSet.as_view({'patch': 'product_warranty_create'},  name='product_warranty_create')),
     
     path('product_stock_in/',
          ProductStockViewSet.as_view({'get': 'list', 'post': 'create'},  name='product_stock_in')),
     path('product_barcode/<barcode>/',
          ProductStockViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='product_barcode')),
     path('product_wise_inventory_list/<product_slug>/',
          ProductStockViewSet.as_view({'get': 'product_wise_inventory_list'},  name='product_wise_inventory_list')),
     path('single_barcode_print/',
          ProductStockViewSet.as_view({'post': 'single_barcode_print'},  name='single_barcode_print')),
     path('multiple_barcode_print/',
          ProductStockViewSet.as_view({'post': 'multiple_barcode_print'},  name='multiple_barcode_print')),
     path('same_barcode_in_single_page/',
          ProductStockViewSet.as_view({'post': 'same_barcode_in_single_page'},  name='same_barcode_in_single_page')),
     path('same_barcode_print/',
          ProductStockViewSet.as_view({'post': 'same_barcode_print'},  name='same_barcode_print')),
     
     path('product_stock_download/<product_slug>/', 
          ProductStockWithProductDownloadViewSet.as_view({'get': 'list'},  name='product_stock_download')),
     path('product_stock_log_download/', 
          ProductStockDownloadViewSet.as_view({'get': 'list'},  name='product_stock_log_download')),
     
     # path('product_stock_log_download/', 
     #      ProductStockLogDownloadViewSet.as_view({'get': 'list'},  name='product_stock_log_download')),
     path('stock_summary/<product_slug>/',
          ProductStockViewSet.as_view({'get': 'stock_summary'},  name='stock_summary')),
     path('stock_summary_report/',
          ProductStockViewSet.as_view({'get': 'stock_summary_report'},  name='stock_summary_report')),
     
     path('product_stock_transfer/',
          ProductStockTransferViewSet.as_view({'post': 'create', 'get': 'list'},  name='product_stock_transfer')),
     path('product_stock_transfer_received/<requisition_no>/',
          ProductStockTransferViewSet.as_view({'patch': 'product_stock_transfer_received'},  name='product_stock_transfer')),
     path('stock_transfer_invoice_print/<requisition_no>/',
          ProductStockTransferViewSet.as_view({'get': 'stock_transfer_invoice_print'},  name='stock_transfer_invoice_print')),
     path('product_stock_transfer/<requisition_no>/',
          ProductStockTransferViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='product_stock_transfer')),
     path('product_stock_transfer_download/',
          ProductStockTransferDownloadViewSet.as_view({'get': 'list'},  name='product_stock_transfer_download')),
     
     # Product Requisition
     
     path('requisition_shop_list/',
          ProductStockRequisitionViewSet.as_view({'get': 'requisition_shop_list'},  name='requisition_shop_list')),
     path('requisition_product_list/<shop_slug>/',
          ProductStockRequisitionViewSet.as_view({'get': 'requisition_product_list'},  name='requisition_product_list')),
     path('product_stock_requisition/',
          ProductStockRequisitionViewSet.as_view({'get': 'list'},  name='product_stock_requisition')),
     path('product_stock_requisition/<shop_slug>/',
          ProductStockRequisitionViewSet.as_view({'post': 'create'},  name='product_stock_requisition')),
     path('product_stock_requisition_update/<requisition_no>/',
          ProductStockRequisitionViewSet.as_view({'patch': 'update'},  name='product_stock_requisition_update')),
     path('product_stock_requisition_transfer/<requisition_no>/',
          ProductStockRequisitionViewSet.as_view({'patch': 'product_stock_requisition_transfer'},  name='product_stock_requisition_transfer')),
     path('product_stock_requisition_details/<requisition_no>/',
          ProductStockRequisitionViewSet.as_view({'get': 'retrieve'},  name='product_stock_requisition_details')),
     
     path('shop_wise_zero_stock_log/',
          ShopWiseZeroStockLogViewSet.as_view({'get': 'list'},  name='shop_wise_zero_stock_log')),
     path('shop_wise_zero_stock_log/<id>/',
          ShopWiseZeroStockLogViewSet.as_view({'get': 'retrieve'},  name='shop_wise_zero_stock_log')),
     path('shop-wise-barcode/<slug:store_slug>/', ShopWiseBarcode.as_view(), name='shop-barcode'),
     
     ]
