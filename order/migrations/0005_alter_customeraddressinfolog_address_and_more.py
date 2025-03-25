# Generated by Django 4.2.7 on 2024-07-13 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddressinfolog',
            name='address',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddressinfolog',
            name='area_name',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddressinfolog',
            name='country_name',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddressinfolog',
            name='district_name',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddressinfolog',
            name='division_name',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddressinfolog',
            name='email',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
    ]
