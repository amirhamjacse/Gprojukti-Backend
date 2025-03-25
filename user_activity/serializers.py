from rest_framework import serializers
from django.db.models import Q
from user.serializers import BaseSerializer
from user_activity.models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    actor  = BaseSerializer(read_only = True)
    
    class Meta:
        model = ActivityLog
        fields = '__all__'