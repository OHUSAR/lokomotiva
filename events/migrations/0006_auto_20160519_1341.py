# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20160519_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='signup_end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_end_time',
            field=models.TimeField(),
        ),
    ]
