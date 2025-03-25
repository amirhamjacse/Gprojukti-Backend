# Generated by Django 4.2.7 on 2024-10-20 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_escalateissue_issue_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='escalateissue',
            name='action_taken',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='escalateissue',
            name='issue_id',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
    ]
