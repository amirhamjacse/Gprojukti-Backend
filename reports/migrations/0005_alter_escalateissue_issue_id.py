# Generated by Django 4.2.7 on 2024-10-20 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_escalateissue_issue_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escalateissue',
            name='issue_id',
            field=models.CharField(default='D4BBE0D772', max_length=10, unique=True),
        ),
    ]
