from django.urls import path, include

app_name = 'location'

urlpatterns = [
    # path('admin/', include('orders.urls.admin'), name='admin.api'),
    path('public/location/', include('location.urls.public.location'), name='public_location.api'),
    path('admin/', include('location.urls.admin.location'), name='admin_location.api'),
]
