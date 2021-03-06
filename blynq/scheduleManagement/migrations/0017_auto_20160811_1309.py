# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-11 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0016_auto_20160811_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentitem',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='scheduleitem',
            name='content_item',
        ),
        migrations.RemoveField(
            model_name='scheduleitem',
            name='schedule_pane',
        ),
        migrations.AlterField(
            model_name='schedulepane',
            name='playlists',
            field=models.ManyToManyField(through='scheduleManagement.SchedulePlaylists', to='playlistManagement.Playlist'),
        ),
        migrations.DeleteModel(
            name='ContentItem',
        ),
        migrations.DeleteModel(
            name='ScheduleItem',
        ),
    ]
