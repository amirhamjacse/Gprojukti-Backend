from django.urls import path, include

from human_resource_management.views.admin.employee import EmployeeInformationViewSet
from order.views.report import *

urlpatterns = [
      path('sales_wise_employee_list/',
            EmployeeInformationViewSet.as_view({'get': 'sales_wise_employee_list'},  name='sales_wise_employee_list')),
      path('sales_wise_employee_details/<slug>/',
            EmployeeInformationViewSet.as_view({'get': 'sales_wise_employee_details'},  name='sales_wise_employee_details')),
      
      path('top_sell_product_list/',
            AdminOrderReportViewSet.as_view({'get': 'top_sell_product_list'},  name='top_sell_product_list')),
      path('product_stock_report_list/',
            AdminOrderReportViewSet.as_view({'get': 'product_stock_report_list'},  name='product_stock_report_list')),
      
      path('payment_type_wise_collection_list/',
            AdminOrderReportViewSet.as_view({'get': 'payment_type_wise_collection_list'},  name='payment_type_wise_collection_list')),
      
      path('order_report_overview_list/',
            AdminOrderReportViewSet.as_view({'get': 'order_report_overview_list'},  name='order_report_overview_list')),
      path('order_report_status_overview_list/',
            AdminOrderReportViewSet.as_view({'get': 'order_report_status_overview_list'},  name='order_report_status_overview_list')),
      
    ]
  