# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('playlistManagement', '0005_auto_20160610_1418'),
        ('screenManagement', '0011_auto_20160708_1906'),
        ('scheduleManagement', '0003_auto_20160610_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleGroup',
            fields=[
                ('schedule_group_id', models.AutoField(serialize=False, primary_key=True)),
                ('group', models.ForeignKey(related_name='schedulegroup_group_id', to='screenManagement.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SchedulePane',
            fields=[
                ('schedule_pane_id', models.AutoField(serialize=False, primary_key=True)),
                ('is_always', models.BooleanField(default=True)),
                ('all_day', models.BooleanField(default=True)),
                ('recurrence_absolute', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
                ('event', models.OneToOneField(related_name='schedulepane', null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Event')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleScreen',
            fields=[
                ('schedule_screen_id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='schedulescreens',
            name='event',
        ),
        migrations.RemoveField(
            model_name='schedulescreens',
            name='group',
        ),
        migrations.RemoveField(
            model_name='schedulescreens',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='schedulescreens',
            name='screen',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='all_day',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='is_always',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='playlists',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='recurrence_absolute',
        ),
        migrations.RemoveField(
            model_name='scheduleplaylists',
            name='schedule',
        ),
        migrations.AddField(
            model_name='schedule',
            name='is_split',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='screens',
            field=models.ManyToManyField(to='screenManagement.Screen', through='scheduleManagement.ScheduleScreen'),
        ),
        migrations.DeleteModel(
            name='ScheduleScreens',
        ),
        migrations.AddField(
            model_name='schedulescreen',
            name='schedule',
            field=models.ForeignKey(related_name='schedulescreen_schedule', to='scheduleManagement.Schedule'),
        ),
        migrations.AddField(
            model_name='schedulescreen',
            name='screen',
            field=models.ForeignKey(related_name='schedulescreen_screen_id', to='screenManagement.Screen'),
        ),
        migrations.AddField(
            model_name='schedulepane',
            name='playlists',
            field=models.ManyToManyField(to='playlistManagement.Playlist', through='scheduleManagement.SchedulePlaylists'),
        ),
        migrations.AddField(
            model_name='schedulepane',
            name='schedule',
            field=models.ForeignKey(related_name='schedulepane_schedule', to='scheduleManagement.Schedule'),
        ),
        migrations.AddField(
            model_name='schedulepane',
            name='split_screen_pane',
            field=models.ForeignKey(to='screenManagement.SplitScreenPane', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='schedulegroup',
            name='schedule',
            field=models.ForeignKey(related_name='schedulegroup_schedule', to='scheduleManagement.Schedule'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='groups',
            field=models.ManyToManyField(to='screenManagement.Group', through='scheduleManagement.ScheduleGroup'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_panes',
            field=models.ManyToManyField(to='screenManagement.SplitScreenPane', through='scheduleManagement.SchedulePane'),
        ),
        migrations.AddField(
            model_name='scheduleplaylists',
            name='schedule_pane',
            field=models.ForeignKey(blank=True, to='scheduleManagement.SchedulePane', null=True),
        ),
    ]
