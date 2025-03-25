from django.urls import path, include

from user.views.public import UserViewSet

urlpatterns = [
    
    path('employee_user_profile/', 
         UserViewSet.as_view({'get':'user_profile'}), name='employee_user_profile'),
]
