# reports/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EscalateIssueViewSet, IssueActionViewSet, EscalateIssueDepartmentViewSet

router = DefaultRouter()
router.register(r'escalate-issue', EscalateIssueViewSet, basename='escalateissue')
router.register(r'issue-action', IssueActionViewSet, basename='issueaction')
router.register(r'department', EscalateIssueDepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
