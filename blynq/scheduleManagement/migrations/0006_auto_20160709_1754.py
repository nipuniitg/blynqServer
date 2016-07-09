# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0005_auto_20160709_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule_panes',
            field=models.ManyToManyField(to='screenManagement.ScreenPane', through='scheduleManagement.SchedulePane'),
        ),
        migrations.AlterField(
            model_name='schedulepane',
            name='split_screen_pane',
            field=models.ForeignKey(to='screenManagement.ScreenPane', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
