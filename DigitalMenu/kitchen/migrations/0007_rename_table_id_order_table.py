# Generated by Django 4.0.2 on 2025-03-05 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0006_rename_table_order_table_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='table_id',
            new_name='table',
        ),
    ]
