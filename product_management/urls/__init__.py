from django.urls import path, include

app_name = 'product'

urlpatterns = [
    # path('admin/', include('orders.urls.admin'), name='admin.api'),
    # path('public/employee/', include('human_resource_management.urls.public.employee'), name='public_employee.api'),
    path('admin/product/', include('product_management.urls.admin.category'), name='admin_product_management.api'),
    path('admin/product_management/', include('product_management.urls.admin.product'), name='admin_product_management.api'),
    path('admin/', include('product_management.urls.admin.brand_seller'), name='admin_product_management.api'),
    
    # Public
    path('public/product_management/', include('product_management.urls.public.category'), name='public_category_management.api'),
    path('public/product_management/', include('product_management.urls.public.product'), name='public_product_management.api'),
    path('public/product_management/', include('product_management.urls.public.brand_seller'), name='public_product_management.api'),
]
