from django.urls import path
from settings_management.views.public import *

urlpatterns = [
     path('slider/',
          PublicSliderViewSet.as_view({'get': 'list'},  name='slider')),
     path('news_letter/',
          NewsLetterViewSet.as_view({'post': 'create'},  name='news_letter')),
     
     path('slider/<slug>/',
          PublicSliderViewSet.as_view({'get': 'retrieve'},  name='slider')),
     
]