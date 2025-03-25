# reports/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EscalateIssue, IssueAction, EscalateIssueDepartment
from .serializers import (
    EscalateIssueSerializer,
    IssueActionSerializer,
    EscalateIssueDepartmentSerializer
)

from user.models import UserAccount
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class EscalateIssueViewSet(viewsets.ModelViewSet):
    queryset = EscalateIssue.objects.select_related(
        'from_department', 'to_department', 'supervisor', 'customer'
    ).prefetch_related('assigned_people', 'issue_actions')
    serializer_class = EscalateIssueSerializer
    permission_classes = [IsAuthenticated]

    # Use filtering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'from_department', 'to_department', 'supervisor', 'customer']
    search_fields = ['subject', 'issue_details']
    ordering_fields = ['issue_create_date', 'days_passed']
    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def solve_issue(self, request, pk=None):
        issue = self.get_object()
        if issue.status == 'SOLVED':
            return Response({"detail": "Issue is already solved."}, status=status.HTTP_400_BAD_REQUEST)

        # Update issue status to SOLVED
        issue.status = 'SOLVED'
        issue.save()

        # Log the action
        action_serializer = IssueActionSerializer(data={
            'issue': issue.id,
            'action_taken': 'Issue solved.',
            'action_by': request.user.id
        })
        if action_serializer.is_valid():
            action_serializer.save(action_by=request.user, issue=issue)
            return Response({"detail": "Issue marked as solved."}, status=status.HTTP_200_OK)
        else:
            return Response(action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def forward_issue(self, request, pk=None):
        issue = self.get_object()

        to_user_id = request.data.get('forwarded_to')
        to_department_id = request.data.get('forwarded_department')

        if not to_user_id and not to_department_id:
            return Response({"detail": "Either 'forwarded_to' or 'forwarded_department' must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        forwarded_to = None
        forwarded_department = None

        if to_user_id:
            forwarded_to = get_object_or_404(UserAccount, id=to_user_id)
        if to_department_id:
            forwarded_department = get_object_or_404(EscalateIssueDepartment, id=to_department_id)

        # Update issue status to FORWARDED
        issue.status = 'FORWARDED'
        if forwarded_department:
            issue.to_department = forwarded_department
        issue.save()

        # Log the action
        action_serializer = IssueActionSerializer(data={
            'issue': issue.id,
            'action_taken': 'Issue forwarded.',
            'action_by': request.user.id,
            'forwarded_to': to_user_id,
            'forwarded_department': to_department_id
        })
        if action_serializer.is_valid():
            action_serializer.save(
                action_by=request.user,
                issue=issue,
                forwarded_to=forwarded_to,
                forwarded_department=forwarded_department
            )
            return Response({"detail": "Issue forwarded successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueActionViewSet(viewsets.ModelViewSet):
    queryset = IssueAction.objects.all()
    serializer_class = IssueActionSerializer
    permission_classes = [IsAuthenticated]

class EscalateIssueDepartmentViewSet(viewsets.ModelViewSet):
    queryset = EscalateIssueDepartment.objects.all()
    serializer_class = EscalateIssueDepartmentSerializer
    permission_classes = [IsAuthenticated]
