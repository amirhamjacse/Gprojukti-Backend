from django.urls import path, include

app_name = 'hrm'

urlpatterns = [
    # path('admin/', include('orders.urls.admin'), name='admin.api'),
    path('public/employee/', include('human_resource_management.urls.public.employee'), name='public_employee.api'),
    path('admin/employee/', include('human_resource_management.urls.admin.employee'), name='admin_employee.api'),
    path('admin/employee/attendance/', include('human_resource_management.urls.admin.attendance'), name='admin_attendance.api'),
    path('admin/employee/settings/', include('human_resource_management.urls.admin.calender'), name='admin_calender.api'),
    path('admin/dashboard/', include('human_resource_management.urls.admin.dashboard'), name='admin_dashboard.api'),
]
