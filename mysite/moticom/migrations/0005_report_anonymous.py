# Generated by Django 3.2.6 on 2021-12-10 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moticom', '0004_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='anonymous',
            field=models.BooleanField(null=True, verbose_name=''),
        ),
    ]