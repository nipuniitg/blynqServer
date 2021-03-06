# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('schedule_id', models.AutoField(serialize=False, primary_key=True)),
                ('schedule_title', models.CharField(max_length=100)),
                ('is_always', models.BooleanField(default=True)),
                ('all_day', models.BooleanField(default=True)),
                ('recurrence_absolute', models.BooleanField(default=False)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
            ],
        ),
        migrations.CreateModel(
            name='SchedulePlaylists',
            fields=[
                ('schedule_playlist_id', models.AutoField(serialize=False, primary_key=True)),
                ('position_index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleScreens',
            fields=[
                ('schedule_screen_id', models.AutoField(serialize=False, primary_key=True)),
                ('event', models.OneToOneField(related_name='schedulescreens', null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.Event')),
            ],
        ),
    ]
