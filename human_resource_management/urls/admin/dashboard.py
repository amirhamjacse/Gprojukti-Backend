from django.urls import path, include

from human_resource_management.views.admin.dashboard import *

urlpatterns = [
        # path('shop_wise_pos_dashboard/<shop_slug>/',
        # DashboardViewSet.as_view({'get': 'shop_wise_pos_dashboard'},  name='shop_wise_pos_dashboard')),
        
        path('shop_wise_pos_dashboard/', DashboardViewSet.as_view({'get': 'shop_wise_pos_dashboard'}), name='shop_wise_pos_dashboard'),
        
        path('shop_wise_notice/', DashboardViewSet.as_view({'get': 'shop_wise_notice'}), name='shop_wise_notice'),
        
        path('shop_wise_employee_performance/', DashboardViewSet.as_view({'get': 'shop_wise_employee_performance'}), name='shop_wise_employee_performance'),
        path('shop_wise_sell_list/', DashboardViewSet.as_view({'get': 'shop_wise_sell_list'}), name='shop_wise_sell_list'),
        path('online_sell_overview_list/', DashboardViewSet.as_view({'get': 'online_sell_overview_list'}), name='online_sell_overview_list'),
        path('online_active_notice_list/', DashboardViewSet.as_view({'get': 'online_active_notice_list'}), name='online_active_notice_list'),
        path('online_upcoming_holiday_list/', DashboardViewSet.as_view({'get': 'upcoming_holiday_list'}), name='online_upcoming_holiday_list'),
        path('online_top_sell_product_list/', DashboardViewSet.as_view({'get': 'online_top_sell_product_list'}), name='online_top_sell_product_list'),
        path('online_dashboard_sell_report/', DashboardViewSet.as_view({'get': 'dashboard_sell_report'}), name='online_dashboard_sell_report'),
        path('online_dashboard_employee_sales_report/', DashboardViewSet.as_view({'get': 'dashboard_employee_sales_report'}), name='online_dashboard_employee_sales_report'),
        path('online_payment_type_wise_received_amount_list/', DashboardViewSet.as_view({'get': 'payment_type_wise_received_amount_list'}), name='online_payment_type_wise_received_amount_list'),
        
        path('offline_sell_overview_list/', DashboardViewSet.as_view({'get': 'online_sell_overview_list'}), name='offline_sell_overview_list'),
        path('offline_active_notice_list/', DashboardViewSet.as_view({'get': 'online_active_notice_list'}), name='offline_active_notice_list'),
        path('offline_upcoming_holiday_list/', DashboardViewSet.as_view({'get': 'upcoming_holiday_list'}), name='offline_upcoming_holiday_list'),
        path('offline_top_sell_product_list/', DashboardViewSet.as_view({'get': 'online_top_sell_product_list'}), name='offline_top_sell_product_list'),
        path('offline_dashboard_sell_report/', DashboardViewSet.as_view({'get': 'dashboard_sell_report'}), name='offline_dashboard_sell_report'),
        path('offline_dashboard_employee_sales_report/', DashboardViewSet.as_view({'get': 'dashboard_employee_sales_report'}), name='offline_dashboard_employee_sales_report'),
        path('offline_payment_type_wise_received_amount_list/', DashboardViewSet.as_view({'get': 'payment_type_wise_received_amount_list'}), name='offline_payment_type_wise_received_amount_list'),
        
        path('dashboard_hrm_employee_attendance/', DashboardViewSet.as_view({'get': 'dashboard_hrm_employee_attendance'}), name='dashboard_hrm_employee_attendance'),
        path('dashboard_hrm_employee_attendance_download/', EmployeeAttendanceViewSet.as_view({'get': 'list'}), name='dashboard_hrm_employee_attendance_download'),
        path('dashboard_hrm_employee_notice/', DashboardViewSet.as_view({'get': 'dashboard_hrm_employee_notice'}), name='dashboard_hrm_employee_notice'),
        path('dashboard_hrm_employee_birthday/', DashboardViewSet.as_view({'get': 'dashboard_hrm_employee_birthday'}), name='dashboard_hrm_employee_birthday'),
        path('dashboard_hrm_upcoming_joining_employee/', DashboardViewSet.as_view({'get': 'dashboard_hrm_upcoming_joining_employee'}), name='dashboard_hrm_upcoming_joining_employee'),
    ]