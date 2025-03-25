# Generated by Django 4.2.7 on 2024-07-09 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier_status', models.CharField(choices=[('PENDING_PICKUP', 'Pending Pickup'), ('IN_TRANSIT', 'In Transit'), ('OUT_OF_DELIVERY', 'Out of Delivery'), ('DELIVERED_TO_CUSTOMER', 'Delivered to Customer'), ('DELAYED', 'Delayed'), ('RETURNED', 'Returned'), ('CANCELLED', 'Cancelled'), ('PROBLEMATIC', 'Problematic'), ('OTHERS', 'Others')], default='PENDING_PICKUP', max_length=30)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourierService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('meta', models.JSONField(default=dict)),
                ('courier_type', models.CharField(choices=[('IN_HOUSE', 'In-House'), ('THIRD_PARTY', 'Third Party')], default='IN_HOUSE', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourierStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('courier_status_code', models.CharField(blank=True, max_length=50, null=True)),
                ('courier_status_display', models.CharField(blank=True, max_length=50, null=True)),
                ('courier_status_change_reason', models.TextField(blank=True, null=True)),
                ('status_change_by', models.JSONField(blank=True, null=True)),
                ('status_change_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('courier_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_mans', to='courier_management.courierservice')),
            ],
        ),
    ]
