# Generated by Django 4.2.7 on 2024-07-09 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settings_management', '0001_initial'),
        ('product_management', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('human_resource_management', '0002_initial'),
        ('location', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='slider',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slider_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shoppanelhook',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_panel_hook_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shoppanelhook',
            name='shop_panel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_panel_hooks', to='settings_management.shoppanel'),
        ),
        migrations.AddField(
            model_name='shoppanelhook',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_panel_hook_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shoppanel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_panel_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shoppanel',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_panel_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shopdayendmessage',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_day_end_message_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shopdayendmessage',
            name='employee_information',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_day_end_messages', to='human_resource_management.employeeinformation'),
        ),
        migrations.AddField(
            model_name='shopdayendmessage',
            name='office_location',
            field=models.ManyToManyField(blank=True, related_name='shop_day_end_messages', to='location.officelocation'),
        ),
        migrations.AddField(
            model_name='shopdayendmessage',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_day_end_message_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shopdayend',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_day_end_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shopdayend',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_day_ends', to='location.officelocation'),
        ),
        migrations.AddField(
            model_name='shopdayend',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_day_end_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newsletter_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newsletter_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hookproduct',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hook_product_created_bys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hookproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hook_products', to='product_management.product'),
        ),
        migrations.AddField(
            model_name='hookproduct',
            name='shop_panel_hook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hook_products', to='settings_management.shoppanelhook'),
        ),
        migrations.AddField(
            model_name='hookproduct',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hook_product_updated_bys', to=settings.AUTH_USER_MODEL),
        ),
    ]
