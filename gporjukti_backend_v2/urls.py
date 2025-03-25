
from django.contrib import admin
from django.urls import path, include,  re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers



router = routers.DefaultRouter()
import debug_toolbar

schema_urlpatterns = [
    path("spectacular/", SpectacularAPIView.as_view(), name="schema"),
    path("",SpectacularSwaggerView.as_view(url_name="schema"),name="doc",),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"),name="redoc",),
    
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


v2_patterns = [
    path('base/', include('base.urls', namespace='base.apis')), # OK
    path('users/', include('user.urls', namespace='user.apis')),
    path('user_activity/', include('user_activity.urls')),
    path('hrm/', include('human_resource_management.urls', namespace='human_resource_management.apis')),
    path('product/', include('product_management.urls', namespace='product_management.apis')),
    path('location/', include('location.urls', namespace='location.apis')),
    path('discount/', include('discount.urls', namespace='discount.apis')), # OK
    path('order/', include('order.urls', namespace='order.apis')),
    path('courier_service/', include('courier_management.urls', namespace='courier_management.apis')),
    path('settings_management/', include('settings_management.urls', namespace='settings_management.apis')),
    path('reports/', include('reports.urls')),
    path('purchase/', include('purchase_management.urls',)),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('rest_framework.urls')),
    path('', include([path('v2.0/', include(v2_patterns))])),
    
]+ schema_urlpatterns

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )  

if settings.DEBUG:
    urlpatterns = urlpatterns + \
                  static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
                  static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
