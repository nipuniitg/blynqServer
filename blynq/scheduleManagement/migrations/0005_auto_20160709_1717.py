# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('screenManagement', '0013_auto_20160709_1717'),
        ('scheduleManagement', '0004_auto_20160708_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleScreens',
            fields=[
                ('schedule_screen_id', models.AutoField(serialize=False, primary_key=True)),
                ('event', models.OneToOneField(related_name='schedulescreens', null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Event')),
                ('group', models.ForeignKey(blank=True, to='screenManagement.Group', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='schedulegroup',
            name='group',
        ),
        migrations.RemoveField(
            model_name='schedulegroup',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='schedulescreen',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='schedulescreen',
            name='screen',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='schedulepane',
            name='is_expired',
        ),
        migrations.AddField(
            model_name='schedule',
            name='split_screen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='screenManagement.SplitScreen', null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='screens',
            field=models.ManyToManyField(to='screenManagement.Screen', through='scheduleManagement.ScheduleScreens'),
        ),
        migrations.AlterField(
            model_name='schedulepane',
            name='event',
            field=models.OneToOneField(related_name='schedulepane_event', null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Event'),
        ),
        migrations.DeleteModel(
            name='ScheduleGroup',
        ),
        migrations.DeleteModel(
            name='ScheduleScreen',
        ),
        migrations.AddField(
            model_name='schedulescreens',
            name='schedule',
            field=models.ForeignKey(related_name='schedulescreens_schedule', to='scheduleManagement.Schedule'),
        ),
        migrations.AddField(
            model_name='schedulescreens',
            name='screen',
            field=models.ForeignKey(related_name='schedulescreens_screen_id', blank=True, to='screenManagement.Screen', null=True),
        ),
    ]
