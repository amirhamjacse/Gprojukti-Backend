# Generated by Django 4.2.7 on 2024-08-07 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsmailsendlog',
            name='status',
            field=models.TextField(blank=True, null=True),
        ),
    ]
