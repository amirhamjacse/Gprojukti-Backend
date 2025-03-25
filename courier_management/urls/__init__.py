from django.urls import path, include

app_name = 'courier_service_management'


urlpatterns = [
    # path('public/', include('discount.urls.public'), name='public_discount.api'),
    path('admin/', include('courier_management.urls.admin'), name='admin_courier_service.api'),
]
