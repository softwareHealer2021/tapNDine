# Generated by Django 4.0.2 on 2025-03-06 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_metrics_earnings_alter_metrics_daily_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metrics',
            name='daily',
        ),
    ]
