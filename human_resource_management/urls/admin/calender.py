from django.urls import path, include

from human_resource_management.views.admin.calender import *

urlpatterns = [
        # Employee Division
        path('event_type/',
                EventTypeViewSet.as_view({'post': 'create', 'get': 'list'},  name='event_type')),
        path('event_type/<slug>/',
                EventTypeViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='event_type')),
        
        path('notice/',
                EventOrNoticeViewSet.as_view({'post': 'create', 'get': 'list'},  name='notice')),
        path('notice/<slug>/',
                EventOrNoticeViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='notice')),
         
        path('event_overview_list/',
                EventOrNoticeViewSet.as_view({'get': 'event_overview_list'},  name='event_overview_list')),
        path('notice_overview_list/',
                EventOrNoticeViewSet.as_view({'get': 'notice_overview_list'},  name='notice_overview_list')),
        
        path('event/',
                EventOrNoticeViewSet.as_view({'post': 'create', 'get': 'list'},  name='event')),
        path('event/<slug>/',
                EventOrNoticeViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='event')),
        
        path('employee_calendar/',
                EmployeeCalendarViewSet.as_view({'post': 'create', 'get': 'list'},  name='employee_calendar')),
        path('employee_calendar/<slug>/',
                EmployeeCalendarViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='employee_calendar')),
        
        path('employee_task/',
                EmployeeTaskViewSet.as_view({'post': 'create', 'get': 'list'},  name='employee_task')),
        path('employee_task/<slug>/',
                EmployeeTaskViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='employee_task')),
     ]
  