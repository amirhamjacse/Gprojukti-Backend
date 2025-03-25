from django.urls import path, include
 
from location.views.public import *

urlpatterns = [
    path('division/',
        PublicDivisionViewSet.as_view({'get': 'list'},  name='division')),
    path('district/',
        PublicDistrictViewSet.as_view({'get': 'list'},  name='district')),
    path('area/',
        PublicAreaViewSet.as_view({'get': 'list'},  name='area')),
    path('district_wise_shop/',
        PublicDistrictWIseShopViewSet.as_view({'get': 'list'},  name='district_wise_shop')),

]
