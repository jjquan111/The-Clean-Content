# Generated by Django 2.2.16 on 2023-11-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dal', '0002_auto_20231127_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garorder',
            name='orderid',
        )
    ]
