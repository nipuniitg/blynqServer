# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('layoutManagement', '0001_initial'),
        ('scheduleManagement', '0010_remove_schedulescreens_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='split_screen',
        ),
        migrations.RemoveField(
            model_name='schedulepane',
            name='screen_pane',
        ),
        migrations.AddField(
            model_name='schedule',
            name='layout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='layoutManagement.Layout', null=True),
        ),
        migrations.AddField(
            model_name='schedulepane',
            name='layout_pane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='layoutManagement.LayoutPane', null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_panes',
            field=models.ManyToManyField(to='layoutManagement.LayoutPane', through='scheduleManagement.SchedulePane'),
        ),
    ]
