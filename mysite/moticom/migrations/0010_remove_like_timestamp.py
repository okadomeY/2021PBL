# Generated by Django 3.2.8 on 2021-11-17 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moticom', '0009_auto_20211117_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='timestamp',
        ),
    ]
