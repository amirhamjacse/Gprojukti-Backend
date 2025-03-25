from django.urls import path
from user_activity.views import ActivityLogViewSet


urlpatterns = [
    path('user_activity_log/', ActivityLogViewSet.as_view({'get':'list'}), name='user_activity_log'),
    path('user_activity_log/<pk>/', ActivityLogViewSet.as_view({'get':'retrieve'}), name='user_activity_log'),
]