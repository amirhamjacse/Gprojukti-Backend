from django.urls import path, include

app_name = 'order'


urlpatterns = [
    path('user/', include('order.urls.public'), name='user_order.api'),
    path('admin/', include('order.urls.admin'), name='admin_order.api'),
    path('report/', include('order.urls.report'), name='report_order.api'),
]
