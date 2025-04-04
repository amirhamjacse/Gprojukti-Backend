# Generated by Django 4.2.7 on 2024-07-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource_management', '0003_alter_employeeattendance_attendance_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeinformation',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeeinformation',
            name='resign_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
