from django.urls import path, include

app_name = 'settings_management'

urlpatterns = [
    path('public/', include('settings_management.urls.public'), name='public.api'),
    path('admin/', include('settings_management.urls.admin'), name='admin.api'),
]
