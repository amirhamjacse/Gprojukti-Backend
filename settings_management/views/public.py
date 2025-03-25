from django.db.models import Q
from base.filters import *
from settings_management.filters import SliderFilter
from settings_management.models import *
from settings_management.serializers import *
from utils.actions import activity_log
from utils.response_wrapper import ResponseWrapper
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from utils.permissions import *
from utils.decorators import log_activity
import re
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PublicSliderViewSet(CustomViewSet):
    queryset = Slider.objects.all().filter(is_active = True).order_by('serial_no')
    lookup_field = 'pk'
    serializer_class = SliderListSerializer
    permission_classes = [AllowAny]
    
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = SliderFilter 
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["list"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    
class NewsLetterViewSet(CustomViewSet):
    queryset = NewsLetter.objects.all()
    lookup_field = 'pk'
    serializer_class = NewsLetterSerializer
    permission_classes = [AllowAny]
    
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.OrderingFilter,
    # )
    # filterset_class = SubscriptionFilter 
    
    def get_serializer_class(self):
        if self.action in ['create']:
            self.serializer_class = NewsLetterCreateSerializer
        else:
            self.serializer_class = NewsLetterSerializer

        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["create"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @log_activity
    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        
        serializer = serializer_class(data=request.data, partial=True)
            
        if serializer.is_valid():
            qs = serializer.save() 
            return ResponseWrapper(data=serializer.data, msg='created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
