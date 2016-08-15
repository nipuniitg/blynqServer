# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-15 06:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcm', '__first__'),
        ('screenManagement', '0022_auto_20160806_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='fcm_device',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fcm.Device'),
        ),
    ]
