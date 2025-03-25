from django.urls import path, include

from location.views import CountryViewSet

urlpatterns = [

    path('country/',
            CountryViewSet.as_view({'post': 'create', 'get': 'list'},  name='country')),
    path('country/<id>/',
            CountryViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='country')),
    ]