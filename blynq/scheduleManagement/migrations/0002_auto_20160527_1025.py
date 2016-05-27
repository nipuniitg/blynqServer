# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('playlistManagement', '0001_initial'),
        ('screenManagement', '0001_initial'),
        ('scheduleManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulescreens',
            name='group',
            field=models.ForeignKey(blank=True, to='screenManagement.Group', null=True),
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
        migrations.AddField(
            model_name='scheduleplaylists',
            name='playlist',
            field=models.ForeignKey(related_name='scheduleplaylists_playlist_id', to='playlistManagement.Playlist'),
        ),
        migrations.AddField(
            model_name='scheduleplaylists',
            name='schedule',
            field=models.ForeignKey(blank=True, to='scheduleManagement.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='created_by',
            field=models.ForeignKey(related_name='schedule_created_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='last_updated_by',
            field=models.ForeignKey(related_name='schedule_last_updated_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='organization',
            field=models.ForeignKey(to='authentication.Organization', null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='playlists',
            field=models.ManyToManyField(to='playlistManagement.Playlist', through='scheduleManagement.SchedulePlaylists'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='screens',
            field=models.ManyToManyField(to='screenManagement.Screen', through='scheduleManagement.ScheduleScreens'),
        ),
    ]
