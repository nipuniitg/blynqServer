# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20160614_1056'),
        ('screenManagement', '0007_auto_20160603_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='last_updated_by',
            field=models.ForeignKey(related_name='group_last_updated_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='last_updated_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 14, 11, 14, 20, 342225, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='screen',
            name='last_updated_by',
            field=models.ForeignKey(related_name='screen_last_updated_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='screen',
            name='last_updated_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 14, 11, 14, 39, 479118, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='created_by',
            field=models.ForeignKey(related_name='group_created_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='authentication.UserDetails', null=True),
        ),
        migrations.AlterField(
            model_name='screen',
            name='activated_by',
            field=models.ForeignKey(related_name='screen_activated_by', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='authentication.UserDetails', null=True),
        ),
    ]
