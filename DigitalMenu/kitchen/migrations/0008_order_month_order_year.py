# Generated by Django 4.0.2 on 2025-03-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0007_rename_table_id_order_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='month',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='year',
            field=models.IntegerField(default=0, max_length=4),
        ),
    ]
