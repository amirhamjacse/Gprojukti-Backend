# Generated by Django 4.2.7 on 2024-07-30 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_management', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
