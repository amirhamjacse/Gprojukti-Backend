# reports/models.py

import uuid
from django.db import models
from user.models import UserAccount

class EscalateIssueDepartment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EscalateIssue(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SOLVED', 'Solved'),
        ('FORWARDED', 'Forwarded'),
        ('UNSOLVED', 'Unsolved')
    ]

    issue_id = models.CharField(max_length=10, unique=True, editable=False)
    issue_create_date = models.DateTimeField(auto_now_add=True)
    days_passed = models.IntegerField(default=0)

    from_department = models.ForeignKey(EscalateIssueDepartment, related_name='from_department', on_delete=models.CASCADE)
    to_department = models.ForeignKey(EscalateIssueDepartment, related_name='to_department', on_delete=models.CASCADE, null=True, blank=True)
    assigned_people = models.ManyToManyField(UserAccount, related_name='assigned_people', blank=True)
    supervisor = models.ForeignKey(UserAccount, related_name='supervisor', null=True, blank=True, on_delete=models.SET_NULL)

    subject = models.CharField(max_length=255)
    issue_details = models.TextField()
    customer = models.ForeignKey(UserAccount, related_name='customer', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    action_taken = models.TextField(blank=True, null=True)  # Ensure this field exists

    def __str__(self):
        return self.issue_id

    def save(self, *args, **kwargs):
        if not self.issue_id:
            unique = False
            while not unique:
                new_id = uuid.uuid4().hex[:10].upper()
                if not EscalateIssue.objects.filter(issue_id=new_id).exists():
                    unique = True
                    self.issue_id = new_id
        super(EscalateIssue, self).save(*args, **kwargs)

class IssueAction(models.Model):
    issue = models.ForeignKey(EscalateIssue, related_name='issue_actions', on_delete=models.CASCADE)
    action_date = models.DateTimeField(auto_now_add=True)
    action_taken = models.TextField()
    action_by = models.ForeignKey(UserAccount, related_name='action_by', on_delete=models.CASCADE)

    # Optional forwarding details
    forwarded_to = models.ForeignKey(UserAccount, related_name='forwarded_to', null=True, blank=True, on_delete=models.SET_NULL)
    forwarded_department = models.ForeignKey(EscalateIssueDepartment, related_name='forwarded_department', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Action on Issue {self.issue.issue_id} by {self.action_by}"
