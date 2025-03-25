from django.contrib import admin
from user_activity.models import ActivityLog

# Register your models here.

# ................***...............User Activity................***............

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['id','actor', 'action_type','request_url','content_type', 'ip_address', 'action_time']
    
    list_filter = ['action_type', 'actor__employee_informations__name', 'action_time']


    class Meta:
        model = ActivityLog
admin.site.register(ActivityLog, ActivityLogAdmin)

