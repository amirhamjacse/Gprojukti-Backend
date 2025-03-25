from django.urls import path, include

app_name = 'admin.base'

urlpatterns = [
    path('public/', include('base.urls.public'), name='public.api'),
    path('admin/', include('base.urls.admin'), name='admin.api'),
    path('bulk_create/', include('base.urls.bulk_create'), name='bulk_create.api'),
]
