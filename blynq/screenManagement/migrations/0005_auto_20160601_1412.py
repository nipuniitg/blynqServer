# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0004_screen_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='activated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='authentication.UserDetails', null=True),
        ),
        migrations.AlterField(
            model_name='screen',
            name='screen_calendar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='schedule.Calendar', null=True),
        ),
    ]
