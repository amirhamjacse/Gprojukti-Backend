# Generated by Django 4.2.7 on 2024-07-09 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('human_resource_management', '0001_initial'),
        ('courier_management', '0001_initial'),
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryman',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_man_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deliveryman',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_mans', to='human_resource_management.employeeinformation'),
        ),
        migrations.AddField(
            model_name='deliveryman',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_man_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courierstatuslog',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courier_status_logs', to='courier_management.courier'),
        ),
        migrations.AddField(
            model_name='courierstatuslog',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier_status_log_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courierstatuslog',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courier_status_log_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courierservice',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_mans', to='base.company'),
        ),
        migrations.AddField(
            model_name='courierservice',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier_service_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courierservice',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courier_service_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courier',
            name='courier_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='couriers', to='courier_management.courierservice'),
        ),
        migrations.AddField(
            model_name='courier',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courier_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courier',
            name='delivery_man',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='couriers', to='courier_management.deliveryman'),
        ),
        migrations.AddField(
            model_name='courier',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='couriers', to='order.order'),
        ),
        migrations.AddField(
            model_name='courier',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courier_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
    ]
