from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserAccount
from user_activity.filters import ActivityLogFilter
from utils.decorators import log_activity
from utils.response_wrapper import ResponseWrapper

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

from django.contrib.auth import get_user_model

# User = get_user_model()
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from utils.permissions import CheckCustomPermission
# import re
from user_activity.serializers import ActivityLogSerializer
from utils.custom_veinlet import CustomViewSet
from rest_framework.permissions import AllowAny
from user_activity.models import ActivityLog
from rest_framework_simplejwt.tokens import RefreshToken
from utils.send_sms import otp_send_sms, send_email
import random
from django.contrib.auth.hashers import make_password
from utils.permissions import *
from rest_framework import permissions, status
from utils.actions import activity_log
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

# Create your views here.

class ActivityLogViewSet(CustomViewSet):
    queryset = ActivityLog.objects.all()
    lookup_field = 'pk'
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = ActivityLogFilter
    
    
    @log_activity
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        
        username = request.user.email or request.user.phone
        user_qs = UserAccount.objects.filter(Q(email=username)|
                                          Q(phone= username)).last()
        
        if not user_qs:
            return ResponseWrapper(
                    status=400,
                    error_msg="User not found"
                )
            
        if request.user.is_superuser == True:
            user_activity_qs = qs.filter()
        else:
            user_activity_qs = qs.filter(actor__id = user_qs.id)
        
        serializer = ActivityLogSerializer(user_activity_qs, many=True)
        
        page_qs = self.paginate_queryset(user_activity_qs)
        serializer = self.serializer_class(instance=page_qs, many=True)

        paginated_data = self.get_paginated_response(serializer.data)
        return ResponseWrapper(data=paginated_data.data, msg="Success", status=200)
