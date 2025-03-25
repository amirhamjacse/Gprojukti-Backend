from django.urls import path, include

app_name = 'discount'


urlpatterns = [
    # path('public/', include('discount.urls.public'), name='public_discount.api'),
    path('admin/', include('discount.urls.admin'), name='admin_discount.api'),
]
