from rest_framework import serializers
from .models import EscalateIssue, EscalateIssueDepartment, IssueAction
from user.models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name']

class EscalateIssueDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscalateIssueDepartment
        fields = ['id', 'name']

class IssueActionSerializer(serializers.ModelSerializer):
    action_by = UserAccountSerializer(read_only=True)
    forwarded_to = UserAccountSerializer(read_only=True)
    forwarded_department = EscalateIssueDepartmentSerializer(read_only=True)

    class Meta:
        model = IssueAction
        fields = [
            'id',
            'issue',
            'action_date',
            'action_taken',
            'action_by',
            'forwarded_to',
            'forwarded_department'
        ]
        read_only_fields = ['issue', 'action_date']

class EscalateIssueSerializer(serializers.ModelSerializer):
    from_department = EscalateIssueDepartmentSerializer(read_only=True)
    to_department = EscalateIssueDepartmentSerializer(read_only=True)
    supervisor = UserAccountSerializer(read_only=True)
    customer = UserAccountSerializer(read_only=True)
    assigned_people = UserAccountSerializer(many=True, read_only=True)
    issue_actions = IssueActionSerializer(many=True, read_only=True)

    # For creating/updating, accept IDs for related fields
    from_department_id = serializers.PrimaryKeyRelatedField(
        queryset=EscalateIssueDepartment.objects.all(), source='from_department', write_only=True
    )
    to_department_id = serializers.PrimaryKeyRelatedField(
        queryset=EscalateIssueDepartment.objects.all(), source='to_department', required=False, allow_null=True, write_only=True
    )
    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=UserAccount.objects.all(), source='supervisor', required=False, allow_null=True, write_only=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=UserAccount.objects.all(), source='customer', required=False, allow_null=True, write_only=True
    )
    assigned_people_ids = serializers.PrimaryKeyRelatedField(
        queryset=UserAccount.objects.all(), source='assigned_people', many=True, write_only=True, required=False
    )

    class Meta:
        model = EscalateIssue
        fields = [
            'id',
            'issue_id',
            'issue_create_date',
            'days_passed',
            'from_department',
            'to_department',
            'supervisor',
            'customer',
            'subject',
            'issue_details',
            'status',
            'action_taken',
            'assigned_people',
            'issue_actions',
            'from_department_id',
            'to_department_id',
            'supervisor_id',
            'customer_id',
            'assigned_people_ids'
        ]
        read_only_fields = ['issue_id', 'issue_create_date', 'days_passed', 'status']

    def create(self, validated_data):
        assigned_people = validated_data.pop('assigned_people', [])
        issue = EscalateIssue.objects.create(**validated_data)
        if assigned_people:
            issue.assigned_people.set(assigned_people)
        return issue

    def update(self, instance, validated_data):
        assigned_people = validated_data.pop('assigned_people', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if assigned_people is not None:
            instance.assigned_people.set(assigned_people)
        return instance
