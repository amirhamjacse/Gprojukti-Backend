from django.urls import path, include
 
from location.views.admin import *

urlpatterns = [
        path('country/',
                CountryViewSet.as_view({'post': 'create', 'get': 'list'},  name='country')),
        path('country/<id>/',
                CountryViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='country')),
        path('division/',
                DivisionViewSet.as_view({'post': 'create', 'get': 'list'},  name='division')),
        path('division/<id>/',
                DivisionViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='division')),
        path('district/',
                DistrictViewSet.as_view({'post': 'create', 'get': 'list'},  name='district')),
        path('district/<id>/',
                DistrictViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='district')),
        path('area/',
                AreaViewSet.as_view({'post': 'create', 'get': 'list'},  name='area')),
        path('area/<id>/',
                AreaViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='area')),
        path('office_location/',
                OfficeLocationViewSet.as_view({'post': 'create', 'get': 'list'},  name='office_location')),
        path('office_location/<slug>/',
                OfficeLocationViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='office_location')),
        path('user_wise_office_location_list/',
                OfficeLocationViewSet.as_view({'get': 'user_wise_office_location_list'},  name='user_wise_office_location_list')),
        
        path('pos_area/',
                POSAreaViewSet.as_view({'post': 'create', 'get': 'list'},  name='pos_area')),
        path('pos_area/<slug>/',
                POSAreaViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='pos_area')),
        
        path('pos_region/',
                POSRegionViewSet.as_view({'post': 'create', 'get': 'list'},  name='pos_region')),
        path('pos_region/<slug>/',
                POSRegionViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='pos_region')),
    ]