from django.urls import path
from user.views.admin import *
from user.views.public import UserViewSet

urlpatterns = [
     path('user_group/',
          UserGroupViewSet.as_view({'post': 'create', 'get': 'list'},  name='user_group')),
     path('user_group/<id>/',
          UserGroupViewSet.as_view({'patch': 'update', 'get': 'retrieve'},  name='user_group')),
     path('user_permission_list/<permission_type>/',
          UserGroupViewSet.as_view({ 'get': 'user_permission_list'},  name='user_permission_list')),
     
     path('user_group_permission_add/<int:group_id>/',
          UserGroupViewSet.as_view({'patch': 'user_group_permission_add'},  name='user_group_permission_add')),
     path('user_group_permission_remove/<int:group_id>/',
          UserGroupViewSet.as_view({'patch': 'user_group_permission_remove'},  name='user_group_permission_remove')),
     path('permission_add_in_user/<int:group_id>/',
          UserGroupViewSet.as_view({'patch': 'permission_add_in_user'},  name='permission_add_in_user')),
     
     path('user_permission/',
          CustomPermissionViewSet.as_view({'get': 'list'},  name='user_permission')),
     path('user_permission_create/',
          CustomPermissionViewSet.as_view({'get': 'create'},  name='user_permission_create')),
     path('user_permission/<id>/',
          CustomPermissionViewSet.as_view({'get': 'retrieve'},  name='user_permission')),
     
     path('user_type/',
          UserTypeViewSet.as_view({'post': 'create', 'get': 'list'},  name='user_type')),
     path('user_type/<id>/',
          UserTypeViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='user_type')),
     
     path('user/',
          AdminUserViewSet.as_view({'post': 'create', 'get': 'list'},  name='user')),
     path('user/<id>/',
          AdminUserViewSet.as_view({'patch': 'update', 'get': 'retrieve', 'delete':'destroy'},  name='user')),
     path('employee_user_information_update/<employee_slug>/',
          AdminUserViewSet.as_view({'patch': 'employee_user_information_update'},  name='employee_user_information_update')),
     path('customer_overview_list/',
          AdminUserViewSet.as_view({'get': 'customer_overview_list'},  name='customer_overview_list')),

     path('user_profile_permissions/', 
          UserViewSet.as_view({'get':'user_profile_permissions'}), name='user_profile_permissions'),
     path('employee_permissions_list/<employee_slug>/', 
          UserViewSet.as_view({'get':'employee_permissions_list'}), name='employee_permissions_list'),
     path('employee_permissions_add_update/<employee_slug>/', 
          UserViewSet.as_view({'patch':'employee_permissions_add_update'}), name='employee_permissions_add_update'),
     
     path('check_permission/<str:codename>/', 
          UserViewSet.as_view({'get':'check_permission'}), name='check_permission'),
     
     path('user_information_download/', 
          UserDownloadViewSet.as_view({'get':'list'}), name='user_information_download'),

]