# Generated by Django 4.2.7 on 2024-07-09 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=355)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('account_number', models.CharField(blank=None, max_length=355, null=True)),
                ('bank_name', models.CharField(blank=None, max_length=355, null=True)),
                ('branch_name', models.CharField(blank=None, max_length=355, null=True)),
                ('routing_number', models.CharField(blank=None, max_length=355, null=True)),
                ('expire_date', models.CharField(blank=None, max_length=355, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('employee_need', models.PositiveBigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeAddressInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_address', models.CharField(max_length=550)),
                ('city', models.CharField(blank=True, max_length=250)),
                ('district_name', models.CharField(blank=True, max_length=250, null=True)),
                ('division_name', models.CharField(blank=True, max_length=250, null=True)),
                ('country_name', models.CharField(blank=True, max_length=250, null=True)),
                ('address_type', models.CharField(choices=[('PERMANENT', 'Permanent'), ('PRESENT', 'Present'), ('OTHERS', 'Others')], default='PERMANENT', max_length=50)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('INITIALIZED', 'Initialized'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='APPROVED', max_length=20)),
                ('attendance_type', models.CharField(choices=[('ON_TIME', 'On Time'), ('OVER_TIME', 'Over Time'), ('LATE', 'Late'), ('EXTRA_OFFICE_DAY', 'Extra Office Day')], default='ON_TIME', max_length=20)),
                ('working_description', models.TextField(blank=True, null=True)),
                ('total_office_hour', models.CharField(blank=True, max_length=20, null=True)),
                ('working_date', models.DateTimeField(blank=True, null=True)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('office_hour_type', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttendanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('status_display', models.CharField(blank=True, max_length=50, null=True)),
                ('working_date', models.DateTimeField(blank=True, null=True)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('status_change_by_info', models.JSONField(blank=True, null=True)),
                ('approved_by_info', models.JSONField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calender_type', models.CharField(choices=[('BUSY', 'Busy'), ('FREE', 'Free')], default='FREE', max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeEducationInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_name', models.CharField(max_length=355)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('board_name', models.CharField(blank=None, max_length=355, null=True)),
                ('grade', models.CharField(blank=None, max_length=355, null=True)),
                ('file', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeGuardianInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('occupation', models.CharField(blank=True, max_length=250)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('nid_number', models.CharField(blank=True, max_length=150, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=150, null=True)),
                ('relationship_type', models.CharField(choices=[('FATHER', 'Father'), ('MOTHER', 'Mother'), ('SISTER', 'Sister'), ('BROTHER', 'Brother'), ('HUSBAND', 'Husband'), ('WIFE', 'Wife'), ('OTHERS', 'Others')], default='FATHER', max_length=50)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=355, unique=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=355, null=True)),
                ('slug', models.SlugField(max_length=555, unique=True)),
                ('nid_number', models.CharField(blank=True, max_length=355, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=355, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=355, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('next_confirmation_date', models.DateField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeInformationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_date', models.DateTimeField(blank=True, null=True)),
                ('employee_info', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeOfficeHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=250, null=True)),
                ('day', models.CharField(blank=True, choices=[('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday'), ('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday')], max_length=50, null=True)),
                ('type', models.CharField(choices=[('REGULAR', 'Regular'), ('EXTRA', 'Extra'), ('SPECIAL', 'SPECIAL')], default='REGULAR', max_length=20)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('grace_time', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_no', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('FEEDBACK', 'Feedback'), ('REJECT', 'Reject'), ('PAUSED', 'Paused'), ('DONE', 'Done')], default='PENDING', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTaskStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=150)),
                ('status_display', models.CharField(max_length=150)),
                ('status_reason', models.TextField(blank=True, null=True)),
                ('status_change_by', models.JSONField(blank=True, null=True)),
                ('status_change_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=555, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EventOrNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('event_url', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('NOTICE', 'Notice'), ('EVENT', 'Event')], default='EVENT', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=550)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Grading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='JobExperienceInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=355)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('address', models.TextField(blank=None, null=True)),
                ('website_url', models.URLField(blank=None, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('resign_date', models.DateField(blank=True, null=True)),
                ('total_job_experience', models.CharField(blank=True, max_length=355, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
