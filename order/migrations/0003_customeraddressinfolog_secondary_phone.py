# Generated by Django 4.2.7 on 2024-07-09 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraddressinfolog',
            name='secondary_phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
